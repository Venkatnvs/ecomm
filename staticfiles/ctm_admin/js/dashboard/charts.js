// dashboard/static/dashboard/js/dashboard.js
function addchats(){
    // Use JSON-serialized data
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
            responsive: false
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
addchats()
