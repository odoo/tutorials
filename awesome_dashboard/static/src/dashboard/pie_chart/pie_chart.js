import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import {
  Component,
  onWillStart,
  useRef,
  useEffect,
  onWillUnmount,
} from "@odoo/owl";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static props = {
    data: Object,
  };

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
    useEffect(() => {
      this.renderChart();
    });
    onWillUnmount(this.onWillUnmount);
  }

  onWillUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: Object.keys(this.props.data),
        datasets: [{ data: Object.values(this.props.data) }],
      },
      options: {
        onClick: (e, elems) => {
          const index = elems[0].index;
          const label = this.chart.data.labels[index];
          const value = this.chart.data.datasets[0].data[index];

          console.log("Clicked slice:", label, value);

          //[TODO] Would have to make an action leading to orders (with domain etc); but need to create orders first
          this.env.services.action.doAction("crm.crm_lead_action_pipeline");
        },
      },
    });
  }
}
