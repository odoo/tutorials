import { Component, onMounted, onPatched, onWillStart, onWillUnmount, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: String,
        data: {
            type: Object,
            optional: true,
        },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });
        onPatched(() => {
            this.chart?.destroy();
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
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
