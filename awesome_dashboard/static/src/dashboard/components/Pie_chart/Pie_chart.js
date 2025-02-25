import {
  Component,
  onWillStart,
  onMounted,
  useRef,
  onWillUnmount,
  useState,
  useEffect,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
  static template = "awesome_dashboard.pie_chart";
  static props = {
    data: Object,
  };

  setup() {
    this.canvasRef = useRef("chartCanvas");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.action = useService("action");

    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

    onMounted(() => {
      this.renderChart();
    });

    onWillUnmount(() => {
      this.chart.destroy();
    });

    useEffect(
      () => {
        if (this.chart) {
          this.updateChart();
        } else {
          this.renderChart();
        }
      },
      () => [this.props]
    );
  }

  renderChart() {
    const labels = Object.keys(this.props);
    const data = Object.values(this.props);
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data: data,
          },
        ],
      },
      options: {
        onClick: (event) => this.onChartClick(event),
      },
    });
  }

  updateChart() {
    this.chart.data.labels = Object.keys(this.props || {});
    this.chart.data.datasets[0].data = Object.values(this.props || {});

    this.chart.update();
  }

  onChartClick(event) {
    const activePoint = this.chart.getElementsAtEventForMode(
      event,
      "nearest",
      { intersect: true },
      true
    );
    if (activePoint.length > 0) {
      const clickedLabel = this.chart.data.labels[activePoint[0].index];
      this.openBlankList();
    }
  }

  openBlankList() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Blank List",
      res_model: "sale.order",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}
