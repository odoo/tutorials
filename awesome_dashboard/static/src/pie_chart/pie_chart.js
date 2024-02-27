/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    useEffect(() => {
      this.renderChart();
    });
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    let labels = Object.keys(this.props.data);
    let data = Object.values(this.props.data);
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        datasets: [
          {
            data: data,
          },
        ],
        labels: labels,
      },
    });
  }
}
