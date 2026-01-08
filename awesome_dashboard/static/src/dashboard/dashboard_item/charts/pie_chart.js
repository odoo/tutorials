
import { Component, onWillStart, onWillUnmount, onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart"

    static props = {
        data: { type: Object, optional: true }
    }

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null

        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"]);
        })


        onMounted(() => this.renderChart());

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });

        onWillUpdateProps(() => this.renderChart());
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        if (this.props.data) {
            let data = {
                datasets: [{
                    data: Object.values(this.props.data)
                }],
                labels: Object.keys(this.props.data)
            }
            
            this.chart = new Chart(this.canvasRef.el, {
                type: 'pie',
                data: data
            });
        }
    }
}