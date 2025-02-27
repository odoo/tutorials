import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {    
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvasRef");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        useEffect(() => this.renderChart());
    }
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        const chartData = this.props.data || {};
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(chartData),
                datasets: [{
                    data: Object.values(chartData),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                }],
            },
        });
    }
}
