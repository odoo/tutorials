import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUnmount,
  useEffect,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class Piechart extends Component {
  static template = "awesome_dashboard.Piechart";
  static props = {
    data: { type: Object },
  };
  setup() {
    this.chart = null;
    this.canvasRef = useRef("canvas");

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    this.chartData = {
      labels: Object.keys(this.props.data),
      datasets: [
        {
          data: Object.values(this.props.data),
        },
      ],
    };

    onMounted(() => {
      this.chart = new Chart(this.canvasRef.el, {
        type: "pie",
        data: this.chartData,
      });
    });
    useEffect(
      () => {
        if (this.chart && this.props.data) {
          this.chart.data.labels = Object.keys(this.props.data);
          this.chart.data.datasets[0].data = Object.values(this.props.data);
          this.chart.update();
        }
      },
      () => [this.props.data]
    );
  }
}
