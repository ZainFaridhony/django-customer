const renderBarChart= (customerdata) => {
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var data = google.visualization.arrayToDataTable(customerdata[0]);
    var options = {
      legend: { position: "none" },
      chart: {},
      hAxis: {
        title: 'Age',
      },
      vAxis: {
        title: 'Income',
      }
    };

    var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
  }
}

const renderGenderBarChart= (genderdata) => {
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(genderdata[0]);

    var options = {
      chart: {},
      legend: { position: 'none' },
      bars: 'horizontal' // Required for Material Bar Charts.
    };

    var chart = new google.charts.Bar(document.getElementById('barchart_material'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
  }
}

const getChartData=()=>{
  fetch('customer_summary')
    .then(res=>res.json())
    .then(data=>{
      renderBarChart([data.age_income_data]);
      renderGenderBarChart([data.gender_data]);
  })
}

document.onload = getChartData();