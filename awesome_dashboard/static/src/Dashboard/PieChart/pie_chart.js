/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart"
    static props = {
        label: String,
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas")
        this.chart = null;

        onWillStart(() => {
            return loadJS("/web/static/lib/Chart/Chart.js")
        })
        
        onMounted(() => {
            this.renderChart()
        })

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        })
    }

    renderChart() {
        const dataLabels = Object.keys(this.props.data)
        const dataValues = Object.values(this.props.data)
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: dataLabels,
                datasets: [
                    {
                        label: this.props.label,
                        data: dataValues,
                        backgroundColor: ["#ff0000", "#00ff00", "#0000ff"]
                    }
                ]
            }
        });
    }
}
