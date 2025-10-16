/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from '@web/core/assets';

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        title: {
            type: String,
        },
        value: {
            type: String | Number,
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
        });
    }

    getChartConfig() {
        if (!this.props.value) return {};
        return {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.value),
                datasets: [{
                    data: Object.values(this.props.value),
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
