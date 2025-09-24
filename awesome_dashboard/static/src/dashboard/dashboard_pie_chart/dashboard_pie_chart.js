import { Component, onWillStart, useEffect, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef('canvas');
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    /**
     * Creates and binds the chart on `canvasRef`.
     */
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getChartConfig());
    }

    /**
     * @returns {object} Chart config for the current data
     */
    getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data)
                }]
            }
        };
    }
}
