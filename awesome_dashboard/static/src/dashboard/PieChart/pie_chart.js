import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets"


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart"

    static props = {
        data: Object,
        label: String
    }

    setup() {
        this.canvaRef = useRef('canvas')
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
        const labels = Object.keys(this.props.data)
        const data = Object.values(this.props.data)

        this.chart = new Chart(this.canvaRef.el, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    label: this.props.label
                }],

            }
        });
    }
}