import {
  Component,
  onMounted,
  onWillStart,
  onWillUnmount,
  useRef,
} from '@odoo/owl';
import { loadJS } from '@web/core/assets';

export class PieChartCard extends Component {
  static template = 'awesome_dashboard.pie_chart_card';

  static props = {
    title: { type: String, optional: true },
    dataset: { type: Array, optional: true },
    labeles: { type: Array, optional: true },
  };

  setup() {
    this.canvasRef = useRef('canvasRef');
    this.chart = null;

    onWillStart(async () => {
      await loadJS('/web/static/lib/Chart/Chart.js');
    });

    onMounted(() => {
      this.renderChart();
    });

    onWillUnmount(() => {
      if (this.chart) {
        this.chart.destroy();
      }
    });
  }

  renderChart() {
    const data = {
      datasets: [
        {
          data: this.props.dataset,
        },
      ],
      labels: this.props.labels,
    };

    const options = {};

    const ctx = this.canvasRef.el.getContext('2d');

    this.chart = new Chart(ctx, {
      type: 'pie',
      data: data,
      options: options,
    });
  }
}
