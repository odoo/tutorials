/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, onWillUnmount,useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object }
    };
    setup() {
        this.chart = null;
        this.canvasRef = useRef("pie_chart_canvas");

        onWillStart(async () => await loadJS("/web/static/lib/Chart/Chart.js"))

        useEffect(() => {
            if (this.canvasRef.el) {
                this.drawChart();
            }
        }, () => [this.props.data]);

        onMounted(() => {
            this.drawChart();
        });

        onWillUnmount(() => {
        if (this.chart) {
            this.chart.destroy();
            }
        });
    }

    drawChart() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }

        const chartData = {
            labels: Object.keys(this.props.data),
            datasets: [{
                data: Object.values(this.props.data),
            }]
        };

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: chartData,
        });
    }
}
