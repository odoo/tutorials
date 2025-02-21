import {
  Component,
  onWillStart,
  useState,
  useRef,
  useEffect,
  onWillUnmount,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class Piechart extends Component {
  static template = "awesome_dashboard.Piechart";
  static components = {};
  static props = {
    orderDetails: { type: Object, shape: { m: Number, s: Number, xl: Number } },
  };

  setup() {
    this.canvasRef = useRef("canvas");
    this.chart = null;

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    useEffect(() => {
      this.renderChart();
      console.log("rendered");
      return () => {
        if (this.chart) {
          this.chart.destroy();
        }
      };
    });
  }

  getChartConfig() {
    return {
      type: "pie",
      data: {
        labels: Object.keys(this.props.orderDetails),
        datasets: [
          {
            data: Object.values(this.props.orderDetails),
          },
        ],
      },
    };
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    const chartConfig = this.getChartConfig();
    this.chart = new Chart(this.canvasRef.el, chartConfig);
  }
}
