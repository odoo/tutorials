import {Component, onWillStart, onMounted, onWillUnmount, useRef} from "@odoo/owl";
import {loadJS} from "@web/core/assets";
import {useService} from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        this.statistics = useService("awesome_dashboard.statistics");

        this.action = useService("action");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            const orders = this.statistics.orders_by_size;

            const labels = ["S", "M", "XL"];

            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels,
                    datasets: [
                        {
                            data: [
                                orders.s || 0,
                                orders.m || 0,
                                orders.xl || 0,
                            ],
                        },
                    ],
                },
                options: {
                    onClick: (event, elements) => {
                        if (!elements.length) {
                            return;
                        }

                        const index = elements[0].index;
                        const size = labels[index];

                        this.openOrdersBySize(size);
                    },
                },
            });
        });

        onWillUnmount(() => {
            this.chart?.destroy();
        });
    }

    onSectionClick(size) {
        this.props.onSectionClick(size);
    }

    openOrdersBySize(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Orders - ${size}`,
            res_model: "sale.order",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [
                ["size", "=", size],
            ],
        });
    }
}
