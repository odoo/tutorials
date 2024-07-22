/** @odoo-module **/

import { Component, onWillStart, useRef, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
        label: String,
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => {
            return loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        useEffect(() => {
            if (this.chart) {
                this.chart.destroy();
            }
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                    },
                ],
            },
        });
    }
}
