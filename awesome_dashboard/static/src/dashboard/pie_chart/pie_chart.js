import { Component, onMounted, onWillStart, onWillUnmount, onWillUpdateProps, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas")

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))

        onMounted(() => this.renderChart());

        onWillUnmount(() => this.chart?.destroy());

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.data.labels = Object.keys(nextProps.data).map(x => x.toUpperCase());
                this.chart.data.datasets[0].data = Object.values(nextProps.data);
                this.chart.update();
            }
        });
    }

    renderChart() {
        this.chart?.destroy();

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels.map(x => x.toUpperCase()),
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
        });
    }
}
