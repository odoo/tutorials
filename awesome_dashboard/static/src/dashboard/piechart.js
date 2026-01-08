import { Component, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = { data: Object };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onMounted(() => {
            this.loadChart();
        });
    }

    async loadChart() {
        await loadJS("/web/static/lib/Chart/Chart.js");
        this.renderChart();
    }

    renderChart() {
        if (!this.canvasRef.el || !this.props.data) {
            console.error("Canvas element or data is missing");
            return;
        }

        if (this.chart) {
            this.chart.destroy();
        }

        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["S", "M", "L"],
                datasets: [{
                    data: [
                        this.props.data?.s || 0,
                        this.props.data?.m || 0,
                        this.props.data?.xl || 0,
                    ],
                    backgroundColor: ["#FF6384", "#4BC0C0", "#36A2EB",],
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "top" },
                },
            },
        });
    }
}
