/** @odoo-module **/

import { Component, useRef, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChartCard extends Component{
    static template = "awesome_dashboard.pie_chart_card";

    static props = {
        title: {type: String, optional: true},
        value: {type: Object, optional: true},
    };

    setup(){
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart.destroy());
    }

    renderChart(){
        const labels = Object.keys(this.props.value);
        const data = Object.values(this.props.value);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                    }
                ]
            }
        });
    }
}
