import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";

  static props = {
    data: Object,
    title: String,
  };

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });
    onMounted(() => {
      this.renderChart();
    });
  }

  renderChart() {
    const labels = Object.keys(this.props.data);
    const data = Object.values(this.props.data);
    const color = ["#ff6384", "#36a2eb", "#cc65fe"];
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            label: this.props.title,
            data: data,
            backgroundColor: color,
          },
        ],
      },
      options: { aspectRatio: 1 },
    });
  }
}
