$.postJSON = function(url, data, callback) {
    $.post(url, data, callback, "json");
};

$(document).ready(function() {
    $('#smooth_btn').click(replot);
    $.getJSON('/energyData', function(data) {
       // Set initial values and draw
        $('#smoothingFactor').val("0.2");
        $('#trendSmoothingFactor').val(0.3);
        $('#seasonSmoothingFactor').val(0.4);
        $('#seasonLength').val(7);
        $('#valuesToForecast').val(0);
        $('#data').val(JSON.stringify(data));
        replot(); 
    });
});

replot = function() {
    $.postJSON( '/holtWinters', 
                {   
                    'smoothingFactor': $('#smoothingFactor').val(),
                    'trendSmoothingFactor': $('#trendSmoothingFactor').val(),
                    'seasonSmoothingFactor': $('#seasonSmoothingFactor').val(),
                    'seasonLength': $('#seasonLength').val(),
                    'valuesToForecast': $('#valuesToForecast').val(),
                    'data': $('#data').val()
                },
                function(data) {
        minX = Math.min.apply(null, data['x'])
        maxX = Math.max.apply(null, data['x'])
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Energy Data',
                x: -20 //center
            },
            xAxis: {
                min: minX,
                max: maxX,
                tickInterval: 60 * 60 * 24,
                labels : {
                    formatter: function() {
                        date = new Date(this.value * 1000);
                        return date.getDate() + "." + (date.getMonth() + 1);
                    }
                }
            },
            yAxis: {
                title: {
                    text: 'Energy Consumption in kwH'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#8080FF'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        new Date(this.x) +': '+ this.y +'kwH';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: 'Original',
                data: data['original']
            }, {
                name: 'Smoothed',
                data: data['smoothed']
            }]
        });
    });
};