import { Component, onWillStart, onWillUnmount, onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { DashboardItem } from "../dashboard-item/dashboard-item";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie-chart";
    static components = { DashboardItem };
    static props = {
        data: { type: Object, values: Number },
    }

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(this.renderChart);
        onWillUpdateProps(this.updateChart);
        onWillUnmount(this.destroyChart);
    }

    renderChart() {
        this.destroyChart();

        const labels = Object.keys(this.props.data);
        const datapoints = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{ data: datapoints }],
            },
        });
    }

    updateChart(newProps) {
        if (this.chart) {
            const datapoints = Object.values(newProps.data);
            Object.assign(this.chart.data.datasets[0], { data: datapoints });
            this.chart.update();
        }
    }
    
    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
}
