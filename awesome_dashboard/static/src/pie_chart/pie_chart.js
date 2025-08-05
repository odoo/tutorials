/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from '@web/core/assets';

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    
    static props = {
        tshirtSales: {
            type: Object,
        }
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")
        });

        useEffect(() => {
            this.createChart();
            return () => this.chart?.destroy();
        }, () => []);
    }

    getChartConfig() {
        if (!this.props.tshirtSales) return {};
        return {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.tshirtSales),
                datasets: [{
                    data: Object.values(this.props.tshirtSales),
                }]
            },
            options: {
                aspectRatio: 2,
            }
        }
    }

    createChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
