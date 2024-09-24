/** @odoo-module **/

import {loadJS} from "@web/core/assets";
import {Component, onWillStart, useEffect, useRef} from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: String,
        data: Object,
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(async () =>
            await loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const labels = Object.keys(this.props.data); // Get the sizes of t-shirts
        const data = Object.values(this.props.data); // Get the number of each size
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: [
                            "rgba(255, 99, 132, 0.2)",
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(255, 206, 86, 0.2)",
                            "rgba(75, 192, 192, 0.2)",
                            "rgba(153, 102, 255, 0.2)",
                            "rgba(255, 159, 64, 0.2)",
                        ],
                    }
                ]
            }
        })
    }
}