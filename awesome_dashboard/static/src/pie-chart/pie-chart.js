import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.pie_chart"
  static props = ['data']

  setup() {
    this.chart = null;
    this.canvasRef = useRef("canvas");
    this.title = "Shirt orders by size"
    onWillStart(async () => loadJS('/web/static/lib/Chart/Chart.js'));

    useEffect(() => {
      this.renderChart();
      return () => {
        if (this.chart) {
          this.chart.destroy();
        }
      };
    });
  }

  renderChart() {
    const labels = Object.keys(this.props.data);
    const data = Object.values(this.props.data);
    const config = {
      type: "doughnut",
      data: {
        datasets: [
          {
            data: data,
            backgroundColor: ["#1f77b4", "#dddddd"],
          },
        ],
        labels: labels,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: 5,
        },
        plugins: {
          title: {
            display: true,
            text: this.title,
            padding: 4,
          },
        },
      },
    };
    this.chart = new Chart(this.canvasRef.el, config);
  }
}
