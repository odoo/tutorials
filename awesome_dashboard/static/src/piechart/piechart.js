/** @odoo-module **/

import { Component, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas"); // Reference to the canvas element
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js"); // Lazy loading Chart.js
        });
    }

    mounted() {
        this.renderChart();
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: this.props.data.map((item) => item.size),
                datasets: [
                    {
                        data: this.props.data.map((item) => item.quantity),
                        backgroundColor: [
                            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"
                        ],
                        borderColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "top" },
                    tooltip: {
                        callbacks: {
                            label: (tooltipItem) => {
                                return `${tooltipItem.label}: ${tooltipItem.raw} items`;
                            },
                        },
                    },
                },
            },
        });
    }
}
