// Redirects cusor to the transaction amount input after submit and on pageload
window.onload = function() {
  document.getElementById('id_transaction_amount').focus();
};

// Creates updates and loads the Chart to browers
document.addEventListener("DOMContentLoaded", function () {
const ctx = document.getElementById('myChart').getContext('2d');
  let myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: [],
      datasets: [{
        label: 'Total',
        data: [],
        backgroundColor: [
          '#36454f',
          '#536878',
          '#708090',
          '#536872',
          '#e3e7ee'],
        borderWidth: 1
      }],

    },
    options: {
      reposive: true,
      maintainAspectRation: true,
      plugins: {
        title: {
          display: true,
          text: "Total Transactions",
          position: "top",
          align: 'start',
          color: "#e3e7ee",
          font: {
            size: 26
          }
        },
        legend: {
          position: "right",
          align: "",
          labels: {
            color: "#e3e7ee",
            font: {
              size: 12,
              weigth: "bold"
            }
          }
        }
      }
    }
  });

  async function updateChart() {
    const response = await fetch('transaction/chart-data/');
    const data = await response.json();
    try {
      myChart.data.labels = data.labels;
      myChart.data.datasets[0].data = data.data;
      myChart.update();
    } catch (error) {
      throw error  
    }
   
  }

  updateChart()
})

