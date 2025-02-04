/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props= {
        labels: Array,
        data: Array
    }
    
    setup() {
        this.pieChartRef= useRef('pieChartRef')
        
        onWillStart(async ()=>{
            await loadJS("/web/static/lib/Chart/Chart.js")
        })
        
        useEffect(()=> this.renderChart())
    }

    /**
     * Creates and binds the chart on `canvasRef`.
     */
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.pieChartRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getChartConfig());
        
    }

    getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: this.props.labels,
                datasets: [{
                    data: this.props.data,
                }],
            },
        }
    }

}
