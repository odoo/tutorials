import {
    Component,
    useRef,
    xml,
    onWillStart,
    onWillUpdateProps,
    onMounted,
    onWillUnmount,
} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static template = xml`
        <canvas t-ref="canvas"></canvas>
    `;

    static props = { clothSize: { type: Object, optional: true } };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        this.actionService = useService("action");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            if (!this.props.clothSize) return;
            this.createChart(this.props.clothSize);
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
            if (!nextProps.clothSize) return;
            setTimeout(() => this.createChart(nextProps.clothSize), 0);
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        });
    }

    openOrders(size) {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders"),
            res_model: "sale.order",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [
                ["order_line.product_id.product_template_attribute_value_ids.name", "=ilike", size],
            ],
        });
    }

    createChart(data) {
        const canvas = this.canvasRef.el;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");

        this.chart = new Chart(ctx, {
            type: "pie",
            options: {
                responsive: true,
                events: ["click"],
                onClick: (event, elements) => {
                    if (!this.chart) return;
                    if (elements.length) {
                        const index = elements[0].index;
                        const size = data.labels[index];
                        this.openOrders(size);
                    }
                },
            },
            data: {
                datasets: [{ data: data.values }],
                labels: data.labels,
            },
        });
    }
}
