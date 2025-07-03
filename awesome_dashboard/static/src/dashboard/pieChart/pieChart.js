import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  useEffect,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class Piechart extends Component {
  static template = "awesome_dashboard.Piechart";
  static props = {
    data: { type: Object },
  };
  setup() {
    this.chart = null;
    this.canvasRef = useRef("canvas");
    this.action = useService("action");

    onWillStart(async () => {
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    const chartData = {
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
        data: chartData,
        options: {
          onClick: (event, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              const size = chartData.labels[idx];
              this.getOrdersBySize(size);
            }
          },
        },
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
  getOrdersBySize(size) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: `Orders with Size ${size.toUpperCase()}`,
      res_model: "sale.order",
      views: [[false, "list"]],
      domain: [
        [
          "order_line.product_template_attribute_value_ids.display_name",
          "ilike",
          size,
        ],
      ],
    });
  }
}
