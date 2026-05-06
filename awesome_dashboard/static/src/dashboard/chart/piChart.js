import { Component, onWillStart, useRef, onMounted } from "@odoo/owl"
import { loadJS } from "@web/core/assets"

export class PiChart extends Component {
    static template = "awesome_dashboard.PiChart";

    static props = {
        data: Object,
        label: {String, optional: true}
    }

    setup(){
        this.canvasRef = useRef("canvas")

        onWillStart(async ()=>{
            await loadJS("/web/static/lib/Chart/Chart.js")
        })

        onMounted(()=>{
            this.renderChart();
        })
    }

    renderChart(){
        const labels = Object.keys(this.props.data)
        const data = Object.values(this.props.data)

        new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    label: this.props.label,
                    data: data,
                    backgroundColor: [
                        '#ff6384', '#36a2eb', '#ffce56'
                    ],
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        })
    }
}
