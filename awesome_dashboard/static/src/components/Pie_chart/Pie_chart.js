import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
  static template = "awesome_dashboard.pie_chart";

  setup() {
    this.canvasRef = useRef("chartCanvas"); // Canvas reference
    this.statistics = useService("awesome_dashboard.statistics");

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
      try {
        this.result = await this.statistics.loadStatistics();
      } catch (err) {
        console.log(`Error occured during the fetching of statistics : ${err}`);
      }
    });

    onMounted(() => {
      const ctx = this.canvasRef.el.getContext("2d");

      this.chart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: Object.keys(this.result.orders_by_size),
          datasets: [
            {
              data: Object.values(this.result.orders_by_size),
              backgroundColor: ["#e4c1f9", "#f694c1", "#a9def9"],
            },
          ],
        },
      });
    });
  }
}
