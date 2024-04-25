/* @odoo-module */

import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets"
export class PieChart extends Component{

    static template = "awesome_dashboard.PieChart"
    static props = {
        label : String,
        data: Object
    }
    setup() {

        this.canvasRef = useRef("canvas")

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))

        onMounted(() => {
            this.renderPieChart()
        })

        onWillUnmount(() => {
            this.chart.destroy()
        })

    }
    
    renderPieChart(){
        const labels = Object.keys(this.props.data)
        const data = Object.values(this.props.data)
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                datasets: [{
                    label: this.props.label,
                    data: data,
                }],
                labels: labels,
            },
        });
    }
}