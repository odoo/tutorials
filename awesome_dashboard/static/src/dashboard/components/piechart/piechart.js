import { Component, onWillStart,onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
    static template = "awesome_dashboard.PieChart"
    setup(){
        this.canvasRef = useRef("canvas")
        onWillStart(async()=>{
            await loadJS("/web/static/lib/Chart/Chart.js")
        })
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.destroy();
            }
            this.renderChart(nextProps.values);
        });
    }
    renderChart(values = this.props.values){
        if (!values) {
            return;
        }
        const labels = Object.keys(this.props.values);
        const data = Object.values(this.props.values);
        const color = ["#007BFF", "#FFA500", "#808090",];
        if (!this.canvasRef.el) {
            return;
        }
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx,{
            type:"pie",
            data:{
                labels:labels,
                datasets: [
                    {
                        label: this.props.title,
                        data:data,
                        backgroundColor: color
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            },
        })
    }
}
