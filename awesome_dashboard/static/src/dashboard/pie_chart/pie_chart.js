import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        data: { type: Object }
    };

    chart = null;

    setup() {
        this.chartRef = useRef("pieChartCanvas");
        // Lazy load
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.shouldRenderChart = true;
        });

        onMounted(() => {
            if (this.shouldRenderChart && window.Chart) {
                this.renderChart();
            } else {
                console.warn("Chart.js not loaded, skipping render.");
            }
        });
    }

    renderChart() {
        const ctx = this.chartRef.el.getContext("2d");

        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new window.Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        "#42A5F5", "#66BB6A", "#AB47BC"
                    ],
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }
}