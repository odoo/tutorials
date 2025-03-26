import { Component, onWillStart, onMounted, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.pie";

  setup() {
    this.canvasRef = useRef("canvas");
    this.statistics = useService("awesome_dashboard.statistics");
    this.state = useState({
      res: this.statistics.data,
    });
    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
      this.chartData = this.state.res.orders_by_size;
    });

    onMounted(() => {
      if (this.chartData) {
        this.renderChart(this.chartData);
      }
    });
  }
  renderChart(ordersBySize) {
    if (!this.canvasRef.el) {
      console.error("Canvas element is not available.");
      return;
    }

    if (this.chart) {
      this.chart.destroy();
    }

    const ctx = this.canvasRef.el.getContext("2d");
    this.chart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["S", "M", "XL"],
        datasets: [
          {
            data: [
              ordersBySize?.s || 0,
              ordersBySize?.m || 0,
              // ordersBySize?.l || 0,
              ordersBySize?.xl || 0,
              ordersBySize?.xxl || 0,
            ],
            backgroundColor: ["#FF6384", "#36A2EB", "#4BC0C0"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
        },
      },
    });
  }
}
