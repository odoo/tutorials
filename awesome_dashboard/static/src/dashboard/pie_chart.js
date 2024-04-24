/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        stats_data: { type: Object },
       };
    
    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        onWillStart(async () =>
            await loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            this.renderChart();
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                datasets: [{
                    data: Object.values(this.props.stats_data)
                }],
                labels: Object.keys(this.props.stats_data)
            },
        });
    }
}