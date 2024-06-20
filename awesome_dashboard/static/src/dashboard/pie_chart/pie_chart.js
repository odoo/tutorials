/** @odoo-module **/

import { Component, onWillStart, useRef, onWillUnmount, useEffect } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.chart = null;
        this.action = useService("action");
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(
            () => {
                this.renderChart();
            },
            () => [this.props.data]
        );
        onWillUnmount(() => this.chart.destroy());
    }

    async renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);

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
                aspectRatio: 2,
                onClick: (evt, el) => {
                    const point = this.chart.getElementsAtEventForMode(
                        evt,
                        "point",
                        {
                            intersect: true,
                        },
                        true
                    );

                    // When we click outside of the chart
                    if (point.length === 0) return;

                    const size = this.chart.data.labels[point[0].index];

                    this.action.doAction({
                        type: "ir.actions.act_window",
                        name: "Related Sales Order",
                        res_model: "sale.order",
                        views: [[false, "list"]],

                        // Just use the name to simulate, no data for this use case on sale app (training)
                        domain: [["name", "ilike", size]],
                        target: "new",
                    });
                },
            },
        });
    }
}
