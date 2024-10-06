class ElasticService:
    def __init__(self, app):
        self.es = app.elasticsearch

    def create_index(self):
        # Vérification si l'index n'existe pas déjà
        if not self.es.indices.exists(index="satellite_passes"):
            # Création de l'index avec un mapping explicite pour les dates
            mapping = {
                "mappings": {
                    "properties": {
                        "satellite_id": {"type": "keyword"},
                        "satellite_name": {"type": "text"},
                        "events": {
                            "type": "nested",
                            "properties": {
                                "time": {
                                    "type": "date",
                                },
                                "event": {"type": "text"},
                                "altitude": {"type": "text"},
                                "azimuth": {"type": "text"},
                                "distance": {"type": "float"}
                            }
                        }
                    }
                }
            }
            self.es.indices.create(index="satellite_passes", body=mapping)

    def index_pass(self, satellite_id, satellite_name, events):
        # Insertion du document satellite avec ses événements dans Elasticsearch
        doc = {
            "satellite_id": satellite_id,
            "satellite_name": satellite_name.replace('-', '_'),
            "events": events
        }
        self.es.index(index="satellite_passes", id=satellite_id, body=doc)

    def index_passes(self, passes):
        satellite_events = {}

        for satellite_pass in passes:
            satellite_id = satellite_pass["satellite_id"]

            if satellite_id not in satellite_events:
                satellite_events[satellite_id] = {
                    "satellite_name": satellite_pass["satellite_name"],
                    "events": []
                }

            satellite_events[satellite_id]["events"].append({
                "time": satellite_pass["time"],
                "event": satellite_pass["event"],
                "altitude": str(satellite_pass["altitude"]),
                "azimuth": str(satellite_pass["azimuth"]),
                "distance": float(satellite_pass["distance"])
            })

        # Indexer tous les satellites et leurs événements dans Elasticsearch
        for satellite_id, data in satellite_events.items():
            self.index_pass(satellite_id, data["satellite_name"], data["events"])

    def search_passes(self, filters):
        query = {
            "bool": {
                "must": []
            }
        }

        # Filtrer par plage de temps et distance dans le champ "events" qui est de type "nested"
        if "start_time" in filters and "end_time" in filters or "min_distance" in filters or "max_distance" in filters:
            nested_query = {
                "nested": {
                    "path": "events",  # Spécification du chemin imbriqué
                    "query": {
                        "bool": {
                            "must": []
                        }
                    }
                }
            }

            # Ajouter le filtre de plage de temps si spécifié
            if "start_time" in filters and "end_time" in filters:
                nested_query["nested"]["query"]["bool"]["must"].append({
                    "range": {
                        "events.time": {
                            "gte": filters["start_time"],  # Format ISO 8601
                            "lte": filters["end_time"]
                        }
                    }
                })

            # Ajouter le filtre de distance si spécifié
            if "min_distance" in filters or "max_distance" in filters:
                range_query = {"range": {"events.distance": {}}}
                if "min_distance" in filters:
                    range_query["range"]["events.distance"]["gte"] = filters["min_distance"]
                if "max_distance" in filters:
                    range_query["range"]["events.distance"]["lte"] = filters["max_distance"]
                nested_query["nested"]["query"]["bool"]["must"].append(range_query)

            # Ajouter la requête imbriquée à la requête principale
            query["bool"]["must"].append(nested_query)

        # Filtrer par nom de satellite si spécifié
        if "satellite_name" in filters and filters["satellite_name"]:
            query["bool"]["must"].append({
                "wildcard": {
                    "satellite_name": f"*{filters['satellite_name']}*"
                }
            })

        from_value = (filters["page"] - 1) * filters["per_page"]
        size_value = filters["per_page"]

        result = self.es.search(
            index="satellite_passes",
            body={"query": query},
            from_=from_value,
            size=size_value
        )
        return result

