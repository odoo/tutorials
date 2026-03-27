import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object },
        label: { type: String, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        useEffect(() => {
            if (this.chart) {
                this.chart.data.labels = Object.keys(this.props.data);
                this.chart.data.datasets[0].data = Object.values(this.props.data);
                this.chart.update();
            }
        }, 
            () => [this.props.data]
        );
        
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });

    }

    renderChart() {
        const config = {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: this.props.label || 'T-Shirt Sizes',
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        '#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#4bc0c0'
                    ],
                }]
            },
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}