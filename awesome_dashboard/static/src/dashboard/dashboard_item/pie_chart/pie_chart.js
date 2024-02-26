/** @odoo-module */

import { loadJS } from "@web/core/assets";
import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUnmount,
} from "@odoo/owl";

export class PieChart extends Component {
  static template = "awesome_dashboard.pieChart";
  static props = {
    label: String,
    data: Object,
  };

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
    onMounted(() => {
      this.renderChart();
    });
  }

  renderChart() {
    const labels = Object.keys(this.props.data);
    const data = Object.values(this.props.data);
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels,
        datasets: [
          {
            label: this.props.label,
            data,
          },
        ],
      },
      options: {
        onClick: (ev, el, c) => {
          if (ev?.type !== "click" || !el[0]) return;
          const index = el[0].index;
          console.log(labels?.[index]);
          // Open the order list view with filter using the size that was clicked on the pie chart
        },
      },
    });
  }
}
