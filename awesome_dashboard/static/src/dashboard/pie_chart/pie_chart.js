import { Component, onWillStart, onMounted, onPatched, useRef, onWillUnmount, } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("chart");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        onPatched(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
        if (this.chart) {
            this.chart.destroy();
            }
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        const data = this.props.data || {};

        if (!Object.keys(data).length) return;

        if (this.chart) {
            this.chart.destroy();
        }

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                }],
            },
        });
    }
}