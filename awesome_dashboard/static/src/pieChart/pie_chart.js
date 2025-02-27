import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUnmount,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static props = {
    data: Object,
    label: String,
  };

  setup() {
    this.url = "/web/static/lib/Chart/Chart.js";
    onWillStart(async () => {
      return await loadJS(this.url);
    });

    this.canvasRef = useRef("canvas");
    onMounted(async () => {
      const sizes = Object.keys(this.props.data);
      const values = Object.values(this.props.data);
      const color = sizes.map((_, index) => getColor(index));
      await this.createChart(sizes, values, color);
    });

    onWillUnmount(() => {
      this.chart && this.chart.destroy();
    });
  }

  async createChart(sizes, values, color) {
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: sizes,
        datasets: [
          {
            label: this.props.label,
            data: values,
            backgroundColor: color,
            hoverBorderColor: "#000",
            hoverBorderWidth: 4,
          },
        ],
      },
    });
  }
}
