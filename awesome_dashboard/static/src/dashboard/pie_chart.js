import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static props = {
        data: Object
    }

    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart?.destroy();
        });
        useEffect(() => {
            this.renderChart();
        }, () => [this.props.data]);
    }

    renderChart() {
        if (!this.props.data) {
            return; 
        }
        if (this.chart) {
            this.chart.destroy();
        }
        const config = {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: 'T-shirt sizes',
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(153, 102, 255)'
                    ],
                }],
            },
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
