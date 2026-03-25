import {
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    onWillUpdateProps,
    useRef,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: String,
        value: {
            type: Object,
            shape: { m: Number, s: Number, xl: Number },
        },
    };

    setup() {
        this.canvasRef = useRef("canvas_ref");
        this.action = useService("action");

        const { m, s, xl } = this.props.value || {};

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            if (!this.canvasRef.el) return;
            const ctx = this.canvasRef.el.getContext("2d");
            if (!ctx) return;

            this.chart = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: ["M", "S", "XL"],
                    datasets: [
                        {
                            data: [m, s, xl],
                            backgroundColor: ["#4CAF50", "#FF5722", "#9C27B0"],
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (ev, elements) => {
                        if (elements.length > 0) {
                            const index = elements[0].index;
                            const label = this.chart.data.labels[index];
                            this.action.doAction({
                                type: "ir.actions.act_window",
                                res_model: "sale.order",
                                views: [[false, "list"]],
                                domain: [
                                    [
                                        "order_line.product_id.product_template_attribute_value_ids.attribute_id.name",
                                        "=",
                                        "size",
                                    ],
                                    [
                                        "order_line.product_id.product_template_attribute_value_ids.name",
                                        "ilike",
                                        label.toLowerCase(),
                                    ],
                                ],
                                name: _t(`Orders with Size ${label}`),
                            });
                        }
                    },
                },
            });
        });
        onWillUpdateProps((nextProps) => {
            let size = nextProps.value || {};
            if (!this.chart && !this.canvasRef) return;
            this.chart.data.datasets[0].data = [size.m, size.s, size.xl];
            this.chart.update();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
}
