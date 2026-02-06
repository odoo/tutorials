import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";

export class PieChart extends Component {
  static template = "awesome_dashboard.AwesomePieChart";
  static props = {
    label: { type: String },
    data: { type: Object },
  };

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(async () => {
      await loadJS(["/web/static/lib/Chart/Chart.js"]);
    });
    onMounted(() => {
      this.renderChart();
    });
    onWillUnmount(() => {
      this.chart.destroy();
    });
  }

  renderChart() {
    const labels = Object.keys(this.props.data);
    console.log(labels)
    const data = Object.values(this.props.data);
    console.log(data)
    const color = labels.map((_, index) => getColor(index));
    const config = {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data,
            backgroundColor: color,
            borderColor: "#fff",
            borderWidth: 2,
            hoverOffset: 8,
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            position: "bottom",
          },
          tooltip: {
            enabled: true,
          },
        },
      },
    };
    this.chart = new Chart(this.canvasRef.el, config);
  }
}
