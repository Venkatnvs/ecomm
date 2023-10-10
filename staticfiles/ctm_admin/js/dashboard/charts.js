function addchats(){
    const userLabels = user_data.map(entry => entry.day);
    const userCounts = user_data.map(entry => entry.count);

    const productLabels = product_data.map(entry => entry.day);
    const productCounts = product_data.map(entry => entry.count);

    // Create user chart
    const userChartCanvas = document.getElementById('userChart');
    const userChart = new Chart(userChartCanvas, {
        type: 'line',
        data: {
            labels: userLabels,
            datasets: [{
                label: 'Users',
                data: userCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Create product chart
    const productChartCanvas = document.getElementById('productChart');
    const productChart = new Chart(productChartCanvas, {
        type: 'bar',
        data: {
            labels: productLabels,
            datasets: [{
                label: 'Products',
                data: productCounts,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

function UniqueUsers(){
    var ctx = document.getElementById('uniqueVisitorsChart').getContext('2d');
    var data = {
        labels: dates,
        datasets: [{
            label: 'Unique Visitors',
            data: counts,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };
    var config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
                    beginAtZero: true
                }
            }
    var uniqueVisitorsChart = new Chart(ctx, config);
}

function DeviceType(){
    var ctx_d = document.getElementById('deviceTypeChart').getContext('2d');
    var data_d = {
        labels: deviceTypes,
        datasets: [{
            label: 'Device Type',
            data: counts_d,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    };

    var config_d = {
        type: 'pie',
        data: data_d,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }
        }
    };

    var deviceTypeChart = new Chart(ctx_d, config_d);
}
function CountryType(labels,data){
    var ctx_d = document.getElementById('CountryChart').getContext('2d');
    var data_d = {
        labels: labels,
        datasets: [{
            label: 'Country',
            data: data,
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    };

    var config_d = {
        type: 'bar',
        data: data_d,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }
        }
    };

    var deviceTypeChart = new Chart(ctx_d, config_d);
}

window.onload = () => {
    addchats()
    UniqueUsers()
    DeviceType()
    GetCountryD()
}

function GetCountryD(){
    var apiUrl = "/analytics/get-country_graph2?format=json";
    var xhr = new XMLHttpRequest();
    xhr.open("GET", apiUrl, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            const labels = response.map((data) => data.country_name);
            const data = response.map((data) => data.count);
            CountryType(labels,data)
        }
    };
    xhr.send();
}
