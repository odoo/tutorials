import { Component, onWillStart, onMounted, onWillUnmount, onPatched, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component{
    static template = "awesome_dashboard.PieChart";

    static props = {
        label: {
            type: String,
        },
        data: {
            type: Object,
        },
    }

    setup(){
        this.canvasRef = useRef("canvas")
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(()=>{
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
        const labels = Object.keys(this.props.data);
        const dataValues = Object.values(this.props.data);

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: dataValues,
                    },
                ]
            }
        });
    }
}