import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });

        // This is the key change. This hook will be executed whenever the
        // component is about to receive new props.
        onWillUpdateProps((nextProps) => {
            if (!this.chart) {
                return;
            }
            // Update the chart's data and labels with the new props
            this.chart.data.labels = Object.keys(nextProps.data);
            this.chart.data.datasets[0].data = Object.values(nextProps.data);
            this.chart.data.datasets[0].backgroundColor = Object.keys(nextProps.data).map((_, index) => getColor(index));

            // Tell Chart.js to re-render with the new data
            this.chart.update();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
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
}