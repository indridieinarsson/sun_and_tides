const harmonicsOptions = {};

tidePredictor = require('tide-predictor.js')
(()=> {
        fetch(
          'https://raw.githubusercontent.com/indridieinarsson/sun_and_tides/master/rvk.json'
        )
        .then(response => {
          return response.json()
        }).then(harmonics => {
          //          console.log('"blefl')
          //          console.log(harmonics)
          //          console.log("---")
          const startDate = new Date()
          const endDate = new Date(startDate.getTime() + (10 * 24 * 60 * 60 * 1000))
                    let pred = tidePredictor(harmonics, {phaseKey: 'phase',})
           const highLow = pred.getExtremesPrediction({
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
          
          highLow.forEach(level => {
            const tableRow = document.createElement('tr')
            tableRow.innerHTML = `
              <td>${level.time}</td>
              <td>${level.label}</td>
              <td>${level.level}</td>
            `
            document.getElementById('tides').appendChild(tableRow)
          })
        })
      })()
