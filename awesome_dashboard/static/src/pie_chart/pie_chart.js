import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        labels: { type: Array, element: String },
        values: { type: Array, element: Number },
        title: { type: String },
    }

    setup() {
        this.chartRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });

    }

    renderChart() {
        this.chart = new Chart(this.chartRef.el, {
            type: "pie",
            data: {
                datasets: [{
                    data: this.props.values
                }],
                labels: this.props.labels,
            }
        })
    }
}