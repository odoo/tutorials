import {
    Component,
    onWillStart,
    onMounted,
    useRef,
    onWillUpdateProps,
} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.action = useService("action");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this._renderChart();
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart && nextProps.data) {
                this.chart.data.datasets[0].data = [
                    nextProps.data.m || 0,
                    nextProps.data.s || 0,
                    nextProps.data.xl || 0,
                ];
                this.chart.update();
            }
        });
    }

    _renderChart() {
        if (!this.props.data) {
            return;
        }

        const ctx = this.canvasRef.el.getContext("2d");
        const data = this.props.data;
        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);
        this.labels = labels;

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["m", "s", "xl"],
                datasets: [
                    {
                        data: [data.m || 0, data.s || 0, data.xl || 0],
                    },
                ],
            },
            options: {
                onClick: (event, elements) => {
                    const size = this.labels[elements[0].index];
                    this.openListView(size);
                },
            },
        });
    }

    openListView(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "propertys",
            res_model: "sale.order",
            views: [[false, "list"]],
            domain: [
                [
                    "order_line.product_id.product_template_attribute_value_ids.product_attribute_value_id.name",
                    "=",
                    size,
                ],
            ],
            target: "new",
        });
    }
}
