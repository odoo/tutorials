import { Component, useRef, onWillStart, onMounted, onWillUpdateProps } from '@odoo/owl'
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = 'awesome_dashboard.PieChart'
    static props = {
        data: Object,
    }

    setup() {
        this.canvasRef = useRef('chartCanvas');
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this._renderChart();
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this._updateChart(nextProps.data);
            }
        });
    }

    _renderChart() {
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: "Orders by T-shirt Size",
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        "#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#9b59b6"
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "right"
                    }
                }
            }
        });
    }

    _updateChart(newData) {
        this.chart.data.labels = Object.keys(newData);
        this.chart.data.datasets[0].data = Object.values(newData);
        this.chart.update();
    }
}
