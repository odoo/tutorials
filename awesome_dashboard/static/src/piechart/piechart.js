import { Component, onMounted, onPatched, onWillStart, onWillUnmount, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets";

export class Piechart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        title: String,
        data: {
            type: Object,
            optional: true,
        },
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => loadJS("/web/static/lib/Chart/Chart.js"));
        onWillUnmount(() => {
            this.chart.destroy();
        });
        onMounted(() => {
            this.renderChart();
        });
        onPatched(() => {
            this.chart?.destroy();
            this.renderChart();
        });

    }

    renderChart() {
        const chartData = this.props.data || {};
        const labels = Object.keys(chartData);
        const data = Object.values(chartData);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.title,
                        data: data,
                    },
                ],
            },
        });
    }
}
