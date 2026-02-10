import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.AwesomePieChart";
  static props = {
    label: { type: String },
    data: { type: Object },
  };

  setup() {
    this.canvasRef = useRef("canvas");
    console.log(this.canvasRef.el);

    onWillStart(async () => {
        await loadJS(["/web/static/lib/Chart/Chart.js"]);
    });
    onMounted(() => {
        console.log(this.canvasRef.el);
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
    const color = ["#1E3D59", "#f8e8baff", "#FF6E40"];

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
            position: "top",
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
