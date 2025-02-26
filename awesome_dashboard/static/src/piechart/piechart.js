/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { Component, onMounted, onWillStart, onWillUnmount, useRef } from "@odoo/owl";

export class PieChart extends Component{
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };
    setup(){
        this.canvasRef = useRef('canvas');
        onWillStart(()=> loadJS("/web/static/lib/Chart/Chart.js"))
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }
    renderChart(){
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el,{
            type: "pie",
            data: {
                  labels: labels,
                datasets: [{
                    label: this.props.label,
                    data: data,
                    backgroundColor: ["#4EA7F2","#EA6175","#43C5B1","#F4A261","#8481DD","#FFD86D"],
                }]
            },
        })
    }
}
