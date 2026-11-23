import {
  Component,
  onWillStart,
  onWillUnmount,
  useEffect,
  useRef,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static props = {
    data: { type: Object, optional: true },
  };
  static defaultProps = {
    data: {},
  };

  setup() {
    this.canvasRef = useRef("canvas");
    this.chart = null;

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    useEffect(() => {
      this.renderChart();
      return () => {
        if (this.chart) {
          this.chart.destroy();
          this.chart = null;
        }
      };
    });

    onWillUnmount(() => {
      if (this.chart) {
        this.chart.destroy();
      }
    });
  }

  renderChart() {
    if (!this.canvasRef.el) {
      return;
    }
    if (this.chart) {
      this.chart.destroy();
    }
    const data = this.props.data || {};
    this.chart = new globalThis.Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: ["S", "M", "XL"],
        datasets: [
          {
            data: [data.s || 0, data.m || 0, data.xl || 0],
            backgroundColor: ["#ff6384", "#36a2eb", "#9966ff"],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  }
}
