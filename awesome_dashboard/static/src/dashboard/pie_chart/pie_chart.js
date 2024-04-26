/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]))
        useEffect(() => this.createPieChart());
        onWillUnmount(() => {
            this.chart.destroy();
        })
    }

    formatPieData() {
        const pieData = {
            datasets: [{ data: [] }],
            labels: []
        };

        for (const size in this.props.data) {
            pieData.datasets[0].data.push(this.props.data[size])
            pieData.labels.push(size)

        }

        return pieData
    }

    createPieChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: this.formatPieData()
        })
    }
}
