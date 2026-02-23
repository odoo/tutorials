import { Component, onMounted, onWillStart, onWillUpdateProps, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        labels: { type: Array },
        values: { type: Array },
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            const chartData = {
                labels: this.props.labels,
                datasets: [{
                    data: this.props.values,
                }],
            };

            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });
        });

        onWillUpdateProps((nextProps) => {
            if (!this.chart) {
                return;
            }
            this.chart.data.labels = nextProps.labels;
            this.chart.data.datasets[0].data = nextProps.values;
            this.chart.update();
        });

    }
}
