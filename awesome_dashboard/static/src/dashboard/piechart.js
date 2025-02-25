import { Component, onWillStart, onMounted, useRef, onPatched } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.canvasRef = useRef("pieChartCanvas");
        this.chart = null;
        this.sizes = {};

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.sizes = this.props.data.orders_by_size;
        });

        onMounted(() => {
            this.drawChart();
        });

        onPatched(() => {
            this.sizes = this.props.data.orders_by_size;
            this.drawChart();
        });
    }

    drawChart() {
        const ctx = this.canvasRef.el;
        if (!ctx) return console.error("Canvas element not found.");
        if (this.chart) this.chart.destroy();

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.sizes),
                datasets: [
                    {
                        data: Object.values(this.sizes),
                        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "top" },
                },
            },
        });
    }
}
