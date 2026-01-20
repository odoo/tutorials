import { loadJS } from "@web/core/assets";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
        useEffect(
            () => {
            this.updateChart();
            },
            () => [this.props.data]
        );
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: ["red", "blue", "green"],
                    },
                ],
            },
        });
    }

    updateChart() {
        if (!this.chart || !this.props.data) return;

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);


        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = data;
        this.chart.data.datasets[0].backgroundColor = ["red", "blue", "green"];;

        this.chart.update();
    }
}
