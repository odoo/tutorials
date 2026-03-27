import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, useRef, onPatched } from "@odoo/owl"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart"
    static props = {
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))
        onMounted(() => this.renderChart())
        onPatched(() => {
            if (this.Chart) {
                this.Chart.destroy();
            }
            this.renderChart();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data)
        const values = Object.values(this.props.data)
        this.Chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                }],
            }
        });
    }
}
