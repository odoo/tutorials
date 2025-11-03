import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static props = { labels: Array, values: Array };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (!this.canvasRef.el) return;

        const ctx = this.canvasRef.el.getContext("2d");

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: this.props.labels,
                datasets: [{
                    label: "Order Distribution",
                    data: this.props.values,
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
                }]
            }
        });
    }
}
