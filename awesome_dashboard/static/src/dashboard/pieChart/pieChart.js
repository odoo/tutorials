import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.pieChart";

    static props = {
        title: { type: String },
        values: { type: Object },
        onSelect: { type: Function, optional: true },
    }

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        useEffect(() => {
            this.renderChart();
        }, () => [this.props.values]);
        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        const labels = Object.keys(this.props.values);

        const data = Object.values(this.props.values);

        if (this.chart) {
            this.chart.destroy();
        }

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#00A09D', 
                        '#E9A13B',
                        '#212529', 
                        '#D9534F',
                        '#5BC0DE',
                    ],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                },
            },
        });
    }

    onChartClick(ev) {
        const chart = Chart.getChart(this.canvasRef.el);
        const activePoints = chart.getElementsAtEventForMode(ev, 'nearest', { intersect: true }, true);
        
        if (activePoints.length > 0) {
            const index = activePoints[0].index;
            const label = chart.data.labels[index];

            if (this.props.onSelect) {
                this.props.onSelect(label);
            }
        }
    }
}
