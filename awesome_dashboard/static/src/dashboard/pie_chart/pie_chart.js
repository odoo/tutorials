/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");

        // Load Chart.js before mounting
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        // Render chart when component is mounted
        onMounted(() => {
            this.renderChart();
        });

        // Destroy the chart when component unmounts
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });

        // Watch for changes in props.data and re-render chart
        useEffect(
            () => {
                this.updateChart();
            },
            () => [this.props.data] // Re-run when `data` changes
        );
    }

    renderChart() {
        if (!this.props.data || !this.canvasRef.el) return;

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const colors = labels.map((_, index) => getColor(index));

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: colors,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            },
        });
    }

    updateChart() {
        if (!this.chart || !this.props.data) return;

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const colors = labels.map((_, index) => getColor(index));

        // Update chart data
        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = data;
        this.chart.data.datasets[0].backgroundColor = colors;

        this.chart.update(); // Refresh the chart
    }
}
