import {
  Component,
  useRef,
  xml,
  onWillStart,
  onWillUpdateProps,
  onMounted,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = xml`
    <t t-name="awesome_dashboard.PieChart" >
      <canvas t-ref="canvas" ></canvas>
    </t>`;
  static props = { clothSize: { type: Object, optional: true } };

  setup() {
    this.canvasRef = useRef("canvas");
    this.chart = null;

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    onMounted(() => {
      if (!this.props.clothSize) return;
      this.createChart(this.props.clothSize);
    });

    onWillUpdateProps((nextProps) => {
      if (!nextProps.clothSize) return;

      if (this.chart) {
        this.chart.destroy();
      }

      this.createChart(nextProps.clothSize);
    });
  }

  createChart(data) {
    const ctx = this.canvasRef.el.getContext("2d");
    this.chart = new Chart(ctx, {
      type: "pie",
      options: {
        responsive: true,
      },
      data: {
        datasets: [
          {
            data: data.values,
          },
        ],
        labels: data.labels,
      },
    });
  }
}
