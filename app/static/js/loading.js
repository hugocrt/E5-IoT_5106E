$(document).ready(function () {
    // Afficher le loader lors de la soumission du formulaire
    $("#satellite-form").on('submit', function () {
        $(".loader").fadeIn(100); // Montre le loader
        $(".index").hide(); // Cache le contenu de la page
    });

    // Lorsque la page est complètement chargée
    $(window).on('load', function () {
        $(".loader").fadeOut(1000); // Fait disparaître le loader
        $(".index").fadeIn(1000); // Fait apparaître le contenu
    });
});
