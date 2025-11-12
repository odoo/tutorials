import { loadJS } from "@web/core/assets";
import { Component, useRef, onWillStart, onMounted, onWillUnmount, useEffect } from "@odoo/owl";

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
            if(this.chart)
            {
                this.chart.destroy();
            }
        });

        // Watch for prop changes and update the chart
        useEffect(
            () => {
                if (this.chart) {
                    this.updateChart(this.props.data);
                }
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
                    },
                ],
            },
        });
    }

    updateChart(newData) {
        this.chart.data.labels = Object.keys(newData);
        this.chart.data.datasets[0].data = Object.values(newData);
        this.chart.update(); // Efficiently update the chart
    }
}
