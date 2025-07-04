/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: { type: Object },
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("chart");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        // Chart data setup
        this.chartData = {
            labels: Object.keys(this.props.data),
            datasets: [
                {
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        "#FF6384", "#36A2EB", "#FFCE56", "#66BB6A", "#BA68C8",
                    ],
                },
            ],
        };

        onMounted(() => {
            this.makeChart();
        });

        // Cleanup
        this.cleanupChart = () => {
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        };

        onWillUnmount(this.cleanupChart);

        // Reactive effect on props.data
        useEffect(() => {
            this.cleanupChart();
            if (this.canvasRef.el) {
                this.makeChart();
            }
        }, () => [this.props.data]);
    }

    makeChart() {
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: this.chartData,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'bottom' },
                    title: {
                        display: true,
                        text: "T-Shirts Sold by Size",
                    },
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const label = this.chartData.labels[index];
                    }
                },
            },
        });
    }
}
