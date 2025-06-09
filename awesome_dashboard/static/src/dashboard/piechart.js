import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class Piechart extends Component {
  static template = "awesome_dashboard.piechart";

  static components = {};

  static props = ["chartData"];

  setup() {
    this.canvasRef = useRef("canvas");
    this.chart = null;
    this.chartData = this.props.chartData;
    onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
    useEffect(
      () => this.renderChart(),
      () => [this.chartData]
    );
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    this.chart = new Chart(this.canvasRef.el, {
      data: this.chartData,
      type: "pie",
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 20,
              usePointStyle: true,
              pointStyle: "rect",
              font: {
                size: 16,
                weight: "bold",
                color: "#fff",
              },
            },
          },
          title: {
            display: true,
            text: "T-Shirt Sales by Size",
            font: {
              size: 16,
              weight: "bold",
            },
            padding: 0,
          },
        },
      },
    });
  }
}
