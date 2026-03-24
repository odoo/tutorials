import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        this.action = useService("action");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const data = this.props.data || {};

        this.labels = Object.keys(data);
        this.values = Object.values(data);

        const ctx = this.canvasRef.el;

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: this.labels,
                datasets: [
                    {
                        data: this.values,
                    },
                ],
            },
            options: {
                responsive: true,
                onClick: (evt, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const size = this.labels[index];

                        this.openOrders(size);
                    }
                },
            },
        });
    }

    openOrders(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Orders",
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: [["order_line.product_id.size", "=", size]],
        });
    }
}
