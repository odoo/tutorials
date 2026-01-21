/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static props = {
    label: String,
    data: Object,
  };

  setup() {
    this.canvasRef = useRef("canvas");

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    onMounted(() => {
      if (!this.props.data || Object.keys(this.props.data).length === 0) {
        console.warn("PieChart: No data provided for chart.");
        console.log(this.props.data);
        return;
      }

      const ctx = this.canvasRef.el.getContext("2d");

      const data = {
        labels: Object.keys(this.props.data),
        datasets: [
          {
            label: "Shirt Sizes",
            data: Object.values(this.props.data),
            backgroundColor: [
              "#3498db",
              "#e67e22",
              "#2ecc71",
              "#9b59b6",
              "#95a5a6",
            ],
          },
        ],
      };

      new window.Chart(ctx, {
        type: "pie",
        data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Shirt orders by size",
            },
          },
        },
      });
    });
  }
}
