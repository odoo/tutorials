import { Component, onWillUnmount, useRef, onWillStart, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";

    setup() {
        this.chart = null;
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
        if (!this.canvasRef.el) {
            return;
        }
        const config = this.canvasRef.el.getContext("2d");

        this.chart = new Chart(config, {
            type: "pie",
            data: {
                labels: ["Red", "Blue", "Yellow"],
                datasets: [{
                    data: [10, 20, 30],
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });
    }
}
