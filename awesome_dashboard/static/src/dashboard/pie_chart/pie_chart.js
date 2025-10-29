/** @odoo-module **/

import { Component, useRef, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { getColor } from "@web/core/colors/colors";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(async () => loadJS(["/web/static/lib/Chart/Chart.js"]))
        onMounted(() => {
            this.renderChart()
        })
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy()
            }
        })
    }

    renderChart() {
        const labels = Object.keys(this.props.data)
        const data = Object.values(this.props.data)
        const color = labels.map((_, index) => getColor(index))
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    }
                ]
            }
        })
    }
}
