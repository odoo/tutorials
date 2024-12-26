/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl"
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        statistics: { type: Object }
    }

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        useEffect(() => {
            this.renderChart()
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            }
        });
    }

    getPieChartData() {
        return {
            labels: [
                "S", "M", "XL"
            ],
            datasets: [{
                data: [
                    this.props.statistics["s"],
                    this.props.statistics["m"],
                    this.props.statistics["xl"],
                ],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'],
                hoverOffset: 4
            }]
        }
    }

    getChartConfig() {
        let config = {
            type: "pie",
            data: this.getPieChartData()
        }
        return config;
    }


    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
