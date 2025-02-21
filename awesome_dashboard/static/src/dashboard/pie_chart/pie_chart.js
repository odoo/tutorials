import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUnmount,
  useEffect
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
    useEffect(
      () => {
        this.updateChart();
      },
      () => [this.props.data]
    );
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

  updateChart() {
    if (!this.chart || !this.props.data) return;

    const labels = this.props.labels;
    const data = this.props.data;
    const colors = labels.map((_, index) => getColor(index));

    // Update chart data
    this.chart.data.labels = labels;
    this.chart.data.datasets[0].data = data[0].data;
    this.chart.data.datasets[0].backgroundColor = colors;

    this.chart.update(); // Refresh the chart
  }
}
