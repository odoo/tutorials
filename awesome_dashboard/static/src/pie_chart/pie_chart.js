/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas")
        onWillStart(() => {
            return loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        useEffect(() => {
            if (this.chart) {
                this.chart.destroy()
            }
            const chartData = Object.entries(this.props.data);
            this.chart = new Chart(this.canvasRef.el, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: chartData.map(([, v]) => v)
                    }],
                    labels: chartData.map(([k]) => k.toUpperCase())
                }
            });
        });
    }
}