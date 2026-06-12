import { Component, onWillStart, onMounted, onWillUnmount, useRef, onPatched } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("soham");
        this.chart = null;

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
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data),
                }],
            },
        });
    }
}
