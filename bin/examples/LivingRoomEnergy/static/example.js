$.postJSON = function(url, data, callback) {
    $.post(url, data, callback, "json");
};

$(document).ready(function() {
    $('#smooth_btn').click(smooth);
    $('#optimize_btn').click(optimize);
    $.getJSON('/energyData', function(data) {
       // Set initial values and draw
        $('#smoothingFactor').val(0.2);
        $('#trendSmoothingFactor').val(0.3);
        $('#seasonSmoothingFactor').val(0.4);
        $('#seasonLength').val(7);
        $('#valuesToForecast').val(0);
        $('#data').val(JSON.stringify(data));
        smooth(); 
    });
});

optimize = function() {
    $.postJSON( '/optimize', 
        {   
            'seasonLength': $('#seasonLength').val(),
            'valuesToForecast': $('#valuesToForecast').val(),
            'data': $('#data').val()
        }, function(data) {
            $('#smoothingFactor').val(data['params']['smoothingFactor'].toString().substring(0,4));
            $('#smoothingFactor_control-group').effect("highlight", {color: '#5BB75B'}, 2000);
            $('#trendSmoothingFactor').val(data['params']['trendSmoothingFactor'].toString().substring(0,4));
            $('#trendSmoothingFactor_control-group').effect("highlight", {color: '#5BB75B'}, 2000);
            $('#seasonSmoothingFactor').val(data['params']['seasonSmoothingFactor'].toString().substring(0,4));
            $('#seasonSmoothingFactor_control-group').effect("highlight", {color: '#5BB75B'}, 2000);
            replot(data);
        });
}

smooth = function () {
    $.postJSON( '/holtWinters', 
        {   
            'smoothingFactor': $('#smoothingFactor').val(),
            'trendSmoothingFactor': $('#trendSmoothingFactor').val(),
            'seasonSmoothingFactor': $('#seasonSmoothingFactor').val(),
            'seasonLength': $('#seasonLength').val(),
            'valuesToForecast': $('#valuesToForecast').val(),
            'data': $('#data').val()
        },
        replot);
}

replot = function(data) {
    $('#error').html("Error: " + data['error'])
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
            categories: getCol(data['smoothed'], 0),
            labels: {
                rotation: 45
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
                    this.x +': '+ round(this.y, 3) +' wH';
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
};

function round(number, precision) {
    return Math.round(number * Math.pow(10, precision)) / Math.pow(10, precision);
}

function getCol(matrix, col){
       var column = [];
       for(var i=0; i<matrix.length; i++){
          column.push(matrix[i][col]);
       }
       return column;
    }