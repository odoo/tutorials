/** @odoo-module **/
import {Component, onMounted, onPatched, onWillStart, onWillUnmount, useRef} from "@odoo/owl"
import {loadJS} from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas")
        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"])
        });
        onMounted(() => this.renderChart())
        onPatched(() => this.updateChart())
        onWillUnmount(() => this.chart.destroy())
    }

    renderChart() {
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        data: Object.values(this.props.data),

                    }
                ]
            }
        });
    }

    updateChart() {
        if (this.chart) {
            this.chart.data.labels = Object.keys(this.props.data);
            this.chart.data.datasets[0].data = Object.values(this.props.data);
            this.chart.update();
        } else {
            this.renderChart();
        }
    }

}