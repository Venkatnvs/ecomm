let locationData;
const map = L.map("map").setView([0, 0], 2);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
        'NvsTrades &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);
var apiUrl = "/analytics/get-country_graph1?format=json";
var xhr = new XMLHttpRequest();
xhr.open("GET", apiUrl, true);
xhr.setRequestHeader("X-CSRFToken", csrftoken);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.onload = function () {
    if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        locationData = response;
        locationData.forEach((location) => {
            const marker = L.marker([location.lat, location.lng]).addTo(map);
            marker.bindPopup(
                `${location.country_code}(${location.city}): ${location.visitors} visitors`
            );
        });
    }
};
xhr.send();