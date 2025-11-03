import { Component, onWillStart, useRef, onMounted, onWillUpdateProps, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        })

        onMounted(() => {
            this.renderChart();
        });

        onWillUpdateProps(() => {
            if (this.chart) {
                this.chart.destroy();
            }
            this.renderChart();
        });

        onWillUnmount(() => {
            this.chart.destroy();
        })
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Orders by Size',
                    data: values,
                    backgroundColor: [
                        '#1f77b4',
                        '#ff7f0e',
                        '#aec7e8',
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
        });
    }
}
