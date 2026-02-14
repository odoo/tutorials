/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");

        const sizes = Object.keys(this.props.data);
        const quantities = Object.values(this.props.data);

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: sizes.map(s => s.toUpperCase()),
                datasets: [{
                    data: quantities,
                    backgroundColor: [
                        "#36A2EB",
                        "#4BC0C0",
                        "#FFCE56",
                        "#FF6384",
                        "#9966FF",
                    ],
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }
}