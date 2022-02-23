
const harmonicsOptions = {};
const jsonfile = "{{ site.url }}/assets/{{ page.datafile }}";
var highLow = {};

// tidePredictor = require('tide-predictor.js')
(()=> {
console.log("first");
        fetch(jsonfile)
        .then(response => {
console.log(response)
          return response.json()
        }).then(harmonics => {
                    console.log('"blefl')
                    console.log(harmonics)
                    console.log("---")
          const startDate = new Date()
          const endDate = new Date(startDate.getTime() + (10 * 24 * 60 * 60 * 1000))
                    let pred = tidePredictor(harmonics, {phaseKey: 'phase',})
           var highLow = pred.getExtremesPrediction({
  start: startDate,
  end: endDate,
  labels: {
    //optional human-readable labels
    high: 'High tide',
    low: 'Low tide',
  },
})
              console.log("tides : ")
              console.log(highLow)
              console.log("---------")
                    //const highLow = tidePredictor(harmonics, {phaseKey: 'phase',
                    //        } ).getExtremesPrediction(new Date('2019-01-01'), new Date('2019-01-10'))
          <!-- highLow.forEach(level => { -->
          <!--   const tableRow = document.createElement('tr') -->
          <!--   tableRow.innerHTML = ` -->
          <!--     <td>${level.time}</td> -->
          <!--     <td>${level.label}</td> -->
          <!--     <td>${level.level}</td> -->
          <!--   ` -->
          <!--   document.getElementById('tides').appendChild(tableRow) -->
          <!-- }) -->
        })
      })()
