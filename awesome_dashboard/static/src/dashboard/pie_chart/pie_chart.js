import {
    Component,
    onWillStart,
    useEffect,
    useRef,
} from "@odoo/owl";

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        labels: Array,
        values: Array,
        label: String,
    };

    setup() {
        this.canvasRef = useRef("pieChartCanvas");
        this.action = useService("action");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            console.log("PieChart effect executed");
            console.log("Canvas element:", this.canvasRef.el);

            if (!this.canvasRef.el) {
                return;
            }

            this.renderChart();

            return () => {
                console.log("Destroying pie chart");

                if (this.chart) {
                    this.chart.destroy();
                    this.chart = null;
                }
            };
        },
        () => [
            this.props.labels,
            this.props.values,
            this.props.label,
        ]
        );
    }

    onPieClick(event, elements) {
        if (!elements.length) {
            return;
        }
        // debugger
        const index = elements[0].index;
        const size = this.props.labels[index];

        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders (Size: %s)", size.toUpperCase()),
            res_model: "sale.order",
            domain: [
                        [
                            "order_line.product_id.product_template_attribute_value_ids.name",
                            "ilike",
                            size,
                        ],
            ],
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const canvas = this.canvasRef.el;

        if (!canvas) {
            console.error("PieChart canvas not found");
            return;
        }
        const labels = this.props.labels;
        const data = this.props.values;
        const colors = labels.map((_, index) => getColor(index));

        this.chart = new Chart(canvas, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: colors,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                onClick: this.onPieClick.bind(this),
            },
        });
    }
}