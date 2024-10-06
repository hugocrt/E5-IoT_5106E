from flask import Blueprint, render_template, request, current_app
from .ip_location import get_location, generate_map
from .satellites import download_satellite_csv_data, calculate_passes
from .services.elastic_service import ElasticService
from datetime import datetime

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    current_page = 'home'

    elastic_service = ElasticService(current_app)
    elastic_service.create_index()

    if request.method == 'POST':
        location = get_location()

        download_satellite_csv_data()
        passes = calculate_passes(location['latitude'], location['longitude'], 30, 2)

        elastic_service.index_passes(passes)

    info = {
        'current_page': current_page,
    }
    return render_template('index.html', info=info)


@main_blueprint.route('/search')
def search():
    current_page = 'search'

    # Récupération des paramètres avec des valeurs par défaut
    start_date = request.args.get('start_date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    satellite_name = request.args.get('satellite_name')
    min_distance = request.args.get('min_distance')
    max_distance = request.args.get('max_distance')
    page = int(request.args.get('page', 1))
    per_page = 20

    # Création des datetime si les paramètres sont fournis
    start_datetime = (
        datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M").isoformat()
        if start_date and start_time else None
    )
    end_datetime = (
        datetime.strptime(f"{start_date} {end_time}", "%Y-%m-%d %H:%M").isoformat()
        if start_date and end_time else None
    )

    # Filtrage des paramètres non nuls
    filters = {
        key: value for key, value in {
            'start_time': start_datetime,
            'end_time': end_datetime,
            'satellite_name': satellite_name,
            'min_distance': min_distance,
            'max_distance': max_distance,
            'page': page,
            'per_page': per_page
        }.items() if value is not None
    }

    # Appel du service de recherche
    elastic_service = ElasticService(current_app)
    result = elastic_service.search_passes(filters)

    # Calcul des informations de pagination
    total_documents = result['hits']['total']['value']
    total_pages = (total_documents + per_page - 1) // per_page

    # Préparation des informations pour le rendu
    info = {
        'current_page': current_page,
        'documents': result['hits']['hits'],
        'total_documents': total_documents,
        'time_to_search': result['took'],
        'current_page_nb': page,
        'per_page': per_page,
        'total_pages': total_pages
    }

    return render_template('search.html', info=info)


@main_blueprint.route('/information')
def information():
    current_page = 'information'
    info = {
        'current_page': current_page
    }
    return render_template('information.html', info=info)


@main_blueprint.route('/references')
def references():
    current_page = 'references'
    info = {
        'current_page': current_page
    }
    return render_template('references.html', info=info)


@main_blueprint.route('/where_am_i')
def where_am_i():
    current_page = 'where_am_i'
    location = get_location()
    map_path = generate_map(location['latitude'], location['longitude'])

    info = {
        'current_page': current_page,
        'location': location,
        'map_path': map_path
    }

    return render_template('where_am_i.html', info=info)
