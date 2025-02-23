import { Component, useRef, onWillStart, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pieChart";
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
            () => [this.props.data]
        );
    }

    renderChart() {
        if (!this.props.data || Object.keys(this.props.data).length === 0) {
            return;
        }

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);

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

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);

        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    }
}
