/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from '@web/core/assets';

export class AwesomeDashboardPieChart extends Component {
    static template = "awesome_dashboard.dashboard_pie_chart";
    static props = {
        title:  { type: String, },
        data: { type: Object, }
    }
    setup(){
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(async() => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        useEffect(() => this.renderChart(this.props.data));
        onWillUnmount(this.onWillUnmount);
    }
    renderChart(data){
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Shirts sold by size',
                    data: Object.values(data),
                }]
            }
        });
    }
    onWillUnmount(){
        if (this.chart) {
            this.chart.destroy();
        }
    }
}
