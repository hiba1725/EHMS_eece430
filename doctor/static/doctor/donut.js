$(document).ready(function() {
    var ctx = $("#chart-line");
    var myLineChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Done", "To do"],
            datasets: [{
                data: [done_app, todo_app],
                backgroundColor: ["rgb(67, 136, 204)", "rgb(220, 220, 220)"]
            }]
        },
    });
});