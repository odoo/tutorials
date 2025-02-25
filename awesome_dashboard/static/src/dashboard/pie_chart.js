/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object
    };

    setup(){
        this.chart = null;
        this.actionService = useService("action");
        this.canvasRef = useRef("canvas");
        onWillStart(async ()=>{
            await loadJS("/web/static/lib/Chart/Chart.js");
        })

        useEffect(() => {
            this.renderChart()
        });
    }

    renderChart(){
        if(this.chart){
            this.chart.destroy();
        }
        const sizeLabels = ["s", "m", "l", "xl", "xxl"]; 
        const chartData = sizeLabels.map(size => this.props.data[size] || 0);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: ["S", "M", "L", "XL", "XXL"],
                datasets: [{
                    label: "T-Shirts Sold",
                    data: chartData,
                    backgroundColor:["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
                }]
            }
    });
    }
}
