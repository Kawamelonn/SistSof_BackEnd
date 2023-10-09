$(function () {


  // =====================================
  // Profit
  // =====================================

  fetch('http://127.0.0.1:8000/SEL4C/api/subcompetencias/') //funcion para jalar los datos 
    .then(response => {
      if(!response.ok){
        throw new Error('Network response was not ok');
      }
      return response.json();
    }) 
    .then(data => {
      const chartData = {
        series: [{name:"Usuarios en subcompetencia:", data:[data.autocontrol, data.liderazgo, data.conciencia_valor_social, data.innovacion_social] }]
      };
      var chartOptions = {
        series: chartData.series,
        
        chart:{
          type: "bar",
          height: 345,
          offsetX: -15,
          toolbar: { show: true },
          foreColor: "#adb0bb",
          fontFamily: 'inherit',
          sparkline: { enabled: false },
        },
        colors: ["#5D87FF", "#49BEFF"],

        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "35%",
            borderRadius: [6],
            borderRadiusApplication: 'end',
            borderRadiusWhenStacked: 'all'
          },
        },
        markers: { size: 0},
        dataLabels:{
          enabled: false,
        },
        legend:{
          show: false,
        },

        grid: {

          borderColor: "rgba(0,0,0,0.1)",
          strokeDashArray: 3,
          xaxis:{
            lines:{
              show: false,
            },
          },
        },

        xaxis: {
          type: "category",
          categories: ["Autocontrol", "Liderazgo", "Conciencia de valor social", "Innovacion Social"],
          labels:{
            style: {cssClass: "grey--text lighten-2--text fill-color"},
          },
        },

        yaxis: {
          show: true,
          min: 0,
          max: 10,
          tickAmount: 4,
          labels:{
            style:{
              cssClass: "grey--text lighten-2--text fill-color",
            },
          },
        },
        stroke:{
          show: true,
          width: 3,
          lineCap: "butt",
          colors: ["transparent"],
        },

        tooltip: { theme: "light" },

        responsive:[
          {
            breakpoint: 600,
            options: {
              plotOptions: {
                bar: {
                  borderRadius: 3,
                }
              },
            }
          }
        ]

      };

      var chart = new ApexCharts(document.querySelector("#chart"), chartOptions);
      chart.render()
    })

    .catch(error => console.error('Error al obtener los datos:', error));


  // =====================================
  // Breakup
  // =====================================
  var breakup1 = {
    color: "#adb5bd",
    series: [38, 40, 25],
    labels: ["2022", "2021", "2020"],
    chart: {
      width: 180,
      type: "donut",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#adb0bb",
    },
    plotOptions: {
      pie: {
        startAngle: 0,
        endAngle: 360,
        donut: {
          size: '75%',
        },
      },
    },
    stroke: {
      show: false,
    },

    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },
    colors: ["#5D87FF", "#ecf2ff", "#F9F9FD"],

    responsive: [
      {
        breakpoint: 991,
        options: {
          chart: {
            width: 150,
          },
        },
      },
    ],
    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },
  };

  var breakup2 = {
    color: "#adb5bd",
    series: [38, 40, 25],
    labels: ["2022", "2021", "2020"],
    chart: {
      width: 180,
      type: "donut",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#adb0bb",
    },
    plotOptions: {
      pie: {
        startAngle: 0,
        endAngle: 360,
        donut: {
          size: '75%',
        },
      },
    },
    stroke: {
      show: false,
    },

    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },
    colors: ["#5D87FF", "#ecf2ff", "#F9F9FD"],

    responsive: [
      {
        breakpoint: 991,
        options: {
          chart: {
            width: 150,
          },
        },
      },
    ],
    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },
  };

  var chart1 = new ApexCharts(document.querySelector("#breakup"), breakup1);
  chart1.render();

  var chart2 = new ApexCharts(document.querySelector("#breakup2"), breakup2);
  chart2.render();



  // =====================================
  // Earning
  // =====================================
  var earning = {
    chart: {
      id: "sparkline3",
      type: "area",
      height: 60,
      sparkline: {
        enabled: true,
      },
      group: "sparklines",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#adb0bb",
    },
    series: [
      {
        name: "Earnings",
        color: "#49BEFF",
        data: [25, 66, 20, 40, 12, 58, 20],
      },
    ],
    stroke: {
      curve: "smooth",
      width: 2,
    },
    fill: {
      colors: ["#f3feff"],
      type: "solid",
      opacity: 0.05,
    },

    markers: {
      size: 0,
    },
    tooltip: {
      theme: "dark",
      fixed: {
        enabled: true,
        position: "right",
      },
      x: {
        show: false,
      },
    },
  };
  new ApexCharts(document.querySelector("#earning"), earning).render();
})



// Hacer una solicitud a la API para obtener los datos
axios.get('http://127.0.0.1:8000/SEL4C/api/subcompetencias/')
  .then(function (response) {
    // Extraer los datos de la respuesta
    const data = response.data;

    // Configuración de la gráfica
    const chartData = {
      series: [{
        name: 'Cantidad de usuarios',
        data: [
          data.autocontrol,
          data.liderazgo,
          data.conciencia_valor_social,
          data.innovacion_social
        ]
      }],
      chart: {
        type: 'bar',
        height: 345,
        offsetX: -15,
        toolbar: { show: true },
        foreColor: '#adb0bb',
        fontFamily: 'inherit',
        sparkline: { enabled: false },
      },
      colors: ['#5D87FF'],
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '35%',
          borderRadius: [6],
          borderRadiusApplication: 'end',
          borderRadiusWhenStacked: 'all'
        },
      },
      markers: { size: 0 },
      dataLabels: { enabled: false },
      legend: { show: false },
      grid: {
        borderColor: 'rgba(0,0,0,0.1)',
        strokeDashArray: 3,
        xaxis: { lines: { show: false } },
      },
      xaxis: {
        type: 'category',
        categories: ['Autocontrol', 'Liderazgo', 'Conciencia y Valor Social', 'Innovación Social'],
        labels: { style: { cssClass: 'grey--text lighten-2--text fill-color' } },
      },
      yaxis: {
        show: true,
        min: 0,
        max: Math.max(data.autocontrol, data.liderazgo, data.conciencia_valor_social, data.innovacion_social) + 10,
        tickAmount: 4,
        labels: { style: { cssClass: 'grey--text lighten-2--text fill-color' } },
      },
      stroke: { show: true, width: 3, lineCap: 'butt', colors: ['transparent'] },
      tooltip: { theme: 'light' },
      responsive: [{
        breakpoint: 600,
        options: { plotOptions: { bar: { borderRadius: 3 } } },
      }],
    };

    // Crear e renderizar la gráfica
    const chart = new ApexCharts(document.querySelector('#chart4'), chartData);  // Usar chartData en lugar de chart4Data
    chart.render();
  })
  .catch(function (error) {
    console.log(error);
  });