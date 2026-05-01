import { loadJS } from "@web/core/assets";
import { Component, useRef, onWillStart, onMounted, onWillUnmount } from "@odoo/owl"

export class PieChart extends Component {
    static template = "estate.PieChart";
    static props = {
        data: { type: Object }
    }

    setup() {
        this.canvasRef = useRef('canvas');
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        })
        onWillUnmount(() => {
            this.chart.destroy();
        })
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                }]
            }
        })
    }
}
