/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  var data = JSON.parse(line_data);

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data["labels"],
      datasets: [{
        data: data["data_1"],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          },
          scaleLabel: {
            display: true,
            labelString: 'Count'
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Date'
          }
        }]
      },
      legend: {
        display: false
      },
      title: {
        display: true,
        text: 'Total Posts'
    }
    }
  })

  var doughnut = document.getElementById('doughnut')
  var d_data = JSON.parse(doughnut_data);
  // eslint-disable-next-line no-unused-vars
  var myChart2 = new Chart(doughnut, {
    type: 'doughnut',
    data: {
      labels: d_data["labels"],
      datasets: [{
        label: 'My First Dataset',
        data: d_data["data"],
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)',
          'rgb(2, 205, 86)'
        ],
        hoverOffset: 4
      }]
    },
    options:{
      title: {
        display: true,
        text: 'Posts Distribution'
      }
    }
  })





})()
