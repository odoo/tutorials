/** @odoo-module **/
import { Component, onWillStart, useRef, onMounted, onPatched } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    setup() {
        this.canvasRef = useRef("chartCanvas");
        this.chartInstance = null; // Store the chart reference

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        onPatched(() => {
            this.updateChart();
        });
    }

    renderChart() {
        if (!this.props.data || Object.keys(this.props.data).length === 0) {
            return;
        }

        const ctx = this.canvasRef.el.getContext("2d");
        this.chartInstance = new Chart(ctx, {
            type: "pie",
            data: this.getChartData(),
            options: { responsive: true }
        });
    }

    updateChart() {
        if (this.chartInstance) {
            this.chartInstance.data = this.getChartData();
            this.chartInstance.update(); // Refresh the chart
        }
    }

    getChartData() {
        return {
            labels: Object.keys(this.props.data),
            datasets: [
                {
                    label: "T-Shirt Sales",
                    data: Object.values(this.props.data),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                    hoverOffset: 22
                },
            ],
        };
    }
}

PieChart.template = "awesome_dashboard.PieChart";
PieChart.props = {
    data: Object,
};
