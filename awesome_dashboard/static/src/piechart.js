import { Component, onWillStart, useRef, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
export class Piechart extends Component {
    static template = "awesome_dashboard.PieChart"
    static props = {
        chartData: Object
    }
    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]))
        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }
    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = {
            type: 'pie',
            data: {
                labels: this.props.chartData.labels,
                datasets: [{
                    data: this.props.chartData.data,
                    backgroundColor: ['blue', 'orange', 'skyblue']
                }]
            },
            options: {
                responsive: true,
            }
        }
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
