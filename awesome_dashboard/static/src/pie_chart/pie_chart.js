import { Component, onWillStart, onMounted, useRef, onWillUnmount } from "@odoo/owl"
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart"
    static props = {
        data: Object,
        label: String,
    }

    setup() {
        this.canvasRef = useRef("canvas_piechart_ref")
        onWillStart(() => loadJS('/web/static/lib/Chart/Chart.js'))

        onMounted(() => this.renderChart())
        onWillUnmount(() => this.myPieChart.destroy())
    }

    renderChart() {
        const data = Object.values(this.props.data)
        const labels = Object.keys(this.props.data)
        const color = labels.map((_, index) => getColor(index))
        this.myPieChart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                datasets: [{
                    data: data,
                    backgroundColor: color,
                    labels: this.props.data
                }],
                labels: labels

            },
        })
    }

}
