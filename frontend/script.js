google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

      var data = new google.visualization.DataTable();
      data.addColumn('timeofday', 'Time of Day');
      data.addColumn('number', 'score');

      data.addRows([
         [{v: [1, 0, 0], f: '1 '}, 75],
        [{v: [2, 0, 0], f: '2 '}, 30],
        [{v: [3, 0, 0], f:'3 '}, 15],
        [{v: [4, 0, 0], f: '4 '}, 10],
        [{v: [5, 0, 0], f: '5 '}, 5],
        [{v: [6, 0, 0], f: '6 '}, 15],
        [{v: [7, 0, 0], f: '7 '}, 45],
        [{v: [8, 0, 0], f: '8 '}, 375],
        [{v: [9, 0, 0], f: '9 '}, 500],
        [{v: [10, 0, 0], f: '10 '}, 450],
        [{v: [11, 0, 0], f: '11 '}, 1595],
        [{v: [12, 0, 0], f: '12 '}, 750],
        [{v: [13, 0, 0], f: '13 '}, 810],
        [{v: [14, 0, 0], f: '14 '}, 700],
        [{v: [15, 0, 0], f: '15 '}, 855],
        [{v: [16, 0, 0], f: '16 '}, 1140],
        [{v: [17, 0, 0], f: '17 '}, 1190],
        [{v: [18, 0, 0], f: '18 '}, 890],
        [{v: [19, 0, 0], f: '19 '}, 1305],
        [{v: [20, 0, 0], f: '20 '}, 1220],
        [{v: [21, 0, 0], f: '21 '}, 815],
        [{v: [22, 0, 0], f: '22 '}, 465],
        [{v: [23, 0, 0], f: '23 '}, 575],
      ]);

      var options = {
        title: 'Rating of the article',
        hAxis: {
          title: 'Time spent on the website',
          format: 'h:mm a',
          viewWindow: {
            min: [1, 0, 0],
            max: [23, 0, 0]
          }
        },
        vAxis: {
          title: 'Rating (scale of 0-2000)'
        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById('chart_div'));

      chart.draw(data, options);
    }