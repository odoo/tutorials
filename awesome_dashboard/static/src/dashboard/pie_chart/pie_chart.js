import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUnmount,
} from "@odoo/owl";
import { getColor } from "@web/core/colors/colors";

import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static props = ["labels", "data"];

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
    onMounted(() => {
      this.renderChart();
    });
    onWillUnmount(() => {
      this.chart.destroy();
    });
  }

  renderChart() {
    const labels = this.props.labels;
    const data = this.props.data;

    const color = labels.map((_, index) => getColor(index));
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            label: this.props.labels,
            data: data[0].data,
            backgroundColor: color,
          },
        ],
      },
    });
  }
}
