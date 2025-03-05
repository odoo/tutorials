import { Component, useRef, onWillStart, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });

        useEffect(
            () => {
                if (this.chart) {
                    this.updateChart();
                } else {
                    this.renderChart();
                }
            },
            () => [this.props]
        );
    }
    renderChart() {
        if (!this.props || Object.keys(this.props).length === 0) {
            return;
        }

        const labels = Object.keys(this.props);
        const data = Object.values(this.props);

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
        });
    }

    updateChart() {
        if (!this.chart) return;

        const labels = Object.keys(this.props);
        const data = Object.values(this.props);

        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    }
}
