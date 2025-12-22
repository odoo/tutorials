import { Component, onWillStart, onWillUnmount, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { DashboardItem } from "../dashboard-item/dashboard-item";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie-chart";
    static components = { DashboardItem };
    static props = {
        data: { type: Array, element: { type: Number }},
        labels: { type: Array, element: { type: String }},
    }

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(this.renderChart);
        onWillUnmount(this.destroyChart);
    }

    renderChart() {
        this.destroyChart();

        this.chart = new Chart(this.canvasRef.el, {
            type: "doughnut",
            data: {
                labels: this.props.labels,
                datasets: [{ data: this.props.data }],
            },
        });
    }
    
    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
}
