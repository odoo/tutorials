import { loadJS } from "@web/core/assets";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
        colors: Array
    };
    setup() {
        this.canvasRef = useRef("pieCanvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });

        onWillUpdateProps((nextProps) => {
            this.updateChart(nextProps.data);
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });
    }
    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: this.props.colors,
                    },
                ],
            },
        });
    }
    updateChart(newData) {
        if (this.chart) {
            this.chart.data.labels = Object.keys(newData);
            this.chart.data.datasets[0].data = Object.values(newData);
            this.chart.update();
        }
    }
}
