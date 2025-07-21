import { Component, onWillStart,onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";


export class PieChartCard extends Component{
    static template = "awesome_dashboard.pie_chart"

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
            this.renderChart(nextProps.data);
        });
    }


    renderChart(){
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = ["#007BFF", "#FFA500", "#808090",];
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
                maintainAspectRatio: false
            },  
        })
    }
}
