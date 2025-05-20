import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: { type: Object, default: {} },
    };

    setup() {
        this.canvasRef = useRef("chartCanvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => this.renderChart());

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });

        useEffect(() => {
            this.updateChart();
        },
        () => [this.props.data]);
    }

    renderChart() {
        const data = this.props.data;

        if (!data || typeof data !== "object" || Object.keys(data).length === 0) {
            console.error("Invalid data:", data);
            return;
        }

        const labels = Object.keys(data);
        const values = Object.values(data);

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    label: "Data",
                    data: values,
                }],
            },
        });
    }

    updateChart() {
        if (!this.chart || !this.props.data) return;

        const data = this.props.data;
        const labels = Object.keys(data);
        const values = Object.values(data);

        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = values;

        this.chart.update();
    }
}
