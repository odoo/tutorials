/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static components = {};
  static props = { data: Object };

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
    onMounted(() => {
      this.renderChart();
    });
  }

  renderChart() {
    this.keys = Object.keys(this.props.data);
    this.values = Object.values(this.props.data);
    const color = this.values.map((k, index) => getColor(index, "sm", "sm"));
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: this.keys,
        datasets: [
          {
            label: this.keys,
            data: this.values,
            backgroundColor: color,
          },
        ],
      },
    });
  }
}
