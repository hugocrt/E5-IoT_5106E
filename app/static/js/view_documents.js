function formatTimes() {
            const startHour = document.getElementById('start_time').value;
            const endHour = document.getElementById('end_time').value;

            // Formatage des heures au format HH:MM:SS
            document.getElementById('start_time').value = startHour + ':00';
            document.getElementById('end_time').value = endHour + ':00';
        }

        function updateTimeLabels() {
            var startTime = document.getElementById('start_time').value;
            var endTime = document.getElementById('end_time').value;
            document.getElementById('start_time_label').textContent = startTime + ":00";
            document.getElementById('end_time_label').textContent = endTime + ":00";
        }
        // Fonction pour mettre à jour les labels des sliders de distance
        function updateDistanceLabels() {
            var minDistance = document.getElementById('min_distance').value;
            var maxDistance = document.getElementById('max_distance').value;
            document.getElementById('min_distance_label').textContent = minDistance + " km";
            document.getElementById('max_distance_label').textContent = maxDistance + " km";
        }

