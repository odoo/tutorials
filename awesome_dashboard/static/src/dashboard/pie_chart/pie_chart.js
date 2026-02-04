import { loadJS } from "@web/core/assets";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";

export class PieChart extends Component {

    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.chartref = useRef("chart");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart.destroy());
        useEffect(
            () => {
                if (!this.chart) return
                this.updateChart()
            },
            () => [this.props.data]
        );
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = ['Red', 'Yellow', 'Blue'];
        this.chart = new Chart(this.chartref.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
        });
    }

    updateChart() {
        this.chart.data.datasets[0].data = Object.values(this.props.data);
        this.chart.update()
    }
}
