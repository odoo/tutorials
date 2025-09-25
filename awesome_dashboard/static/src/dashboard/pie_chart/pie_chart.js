import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: {},
        size: { type: Number, optional: true },
    };

    setup() {
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        this.ctx = useRef("pieChart");
        this.action = useService("action");
        this.chart = null;
        onMounted(() => {
            if (this.chart) {
                this.chart.destroy();
            }
            const dataset = {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        data: Object.values(this.props.data),
                    },
                ],
            };
            this.chart = new Chart(this.ctx.el, {
                type: "pie",
                data: dataset,
                options: {
                    onClick: (event) => {
                        const canvasPosition = this.chart.getElementsAtEventForMode(
                            event,
                            'nearest',
                            { intersect: true },
                            true
                        );
                        const variant = Object.keys(this.props.data)[
                            canvasPosition[0].index
                        ]
                        this.action.doAction({
                            type: "ir.actions.act_window",
                            name: _t("Sales"),
                            res_model: "sale.order",
                            views: [
                                [false, "list"],
                                [false, "form"],
                            ],
                            domain: [
                                ['order_line.product_id.name', 'ilike', 'T-Shirt'],
                                ['order_line.product_id.product_template_attribute_value_ids.name',
                                    'ilike',
                                    variant]
                            ]
                        });
                    }
                }
            });

        });
    }
}
