/** @odoo-module **/

import {Component, onWillStart, onWillUnmount, useEffect, useRef} from "@odoo/owl";
import {loadJS} from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.dashboard.dashboard_item.pie_chart";

    static props = {
        'stats': {
            type: Object
        }
    }

    setup() {
        this.canvasRef = useRef("canvas");

        this.chart = null;

        onWillStart(this.willStart)
        useEffect(() => this.renderChart());
        onWillUnmount(this.willUnmount);
    }

    async willStart() {
        await loadJS('/web/static/lib/Chart/Chart.js')
    }

    willUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    getChartConfig() {
        const values = []
        const labels = []

        for (const [label, value] of Object.entries(this.props.stats)) {
            values.push(value)
            labels.push(label)
        }

        return {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: values
                }],

                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: labels
            },
            options: {
                maintainAspectRatio: false,
            }
        }
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = this.getChartConfig();
        console.log(config)
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
