import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, onPatched, onWillUnmount, useRef } from "@odoo/owl";
import { getColor } from "@web/core/colors/colors"

export class PieChart extends Component {
    static template = 'PieChart'
    static props = {
        label: { type: String },
        data: { type: Object }
    }

    setup() {
        debugger
        this.canvasRef = useRef("canvas")
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });
        onPatched(() => {
            this.chart.destroy();
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const label = Object.keys(this.props.data)
        const data = Object.values(this.props.data)
        const color = label.map((_, index) => getColor(index));
        console.log(label)
        console.log(data)
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: label,
                datasets: [{
                    data: data,
                    backgroundColor: color,
                }]

            }
        })
    }

}
