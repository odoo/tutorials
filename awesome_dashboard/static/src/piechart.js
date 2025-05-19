import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets"
import { getColor } from "@web/core/colors/colors"

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        data: Object,
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart.destroy());
    }

    renderChart() {
        const chartLabels = Object.keys(this.props.data.orders_by_size)
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: chartLabels,
                datasets: [
                    {
                        label: "Sizes Chart",
                        data: Object.values(this.props.data.orders_by_size),
                        backgroundColor: chartLabels.map((_, index) => getColor(index)),
                    }
                ]
            }
        });
    }
}
