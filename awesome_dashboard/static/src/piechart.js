/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.canvasRef = useRef("canvas");
        this.chart = null;
        this.chartData = null;  // Store data to use after mounting

        onWillStart(async () => {
            // Load Chart.js dynamically
            await loadJS("/web/static/lib/Chart/Chart.js");

            // Fetch statistics data and store it for later use
            const result = await this.statisticsService.data;
            this.chartData = result.orders_by_size;
        });

        onMounted(() => {
            // Now the canvas is available, so we can render the chart
            if (this.chartData) {
                this.renderChart(this.chartData);
            }
        });

    }

    renderChart(ordersBySize) {
        if (!this.canvasRef.el) {
            console.error("Canvas element is not available.");
            return;
        }

        if (this.chart) {
            this.chart.destroy();
        }

        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["S", "M", "L", "XL", "XXL"],
                datasets: [{
                    data: [
                        ordersBySize?.s || 0,
                        ordersBySize?.m || 0,
                        ordersBySize?.l || 0,
                        ordersBySize?.xl || 0,
                        ordersBySize?.xxl || 0
                    ],
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "top",
                    },
                },
            },
        });
    }
}
