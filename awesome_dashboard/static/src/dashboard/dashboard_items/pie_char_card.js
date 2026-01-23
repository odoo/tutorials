import { Component, onWillStart, useRef, onMounted, onWillPatch, useState } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard"

    static props = {
        title: String,
        value: {type: Object, optional: true}
    }

    chart = null;

    drawChart() {
        if(!this.props.value) return;

        if(this.chart) {
            this.chart.data.datasets[0].data = Object.values(this.props.value);
            this.chart.update();
            return;
        }

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.value),
                datasets: [
                    {
                        label: 'Shirts',
                        data: Object.values(this.props.value)
                    }
                ]
            }
        })
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.drawChart())
        onWillPatch(() => this.drawChart())
    }
}
