import { Component, useState, onWillStart, useRef, onMounted, onPatched, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        title: {type: String, optional: true},
        data: {
            type: Object,
            values: { type: Number },
            optional: true
        }
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => loadJS("/web/static/lib/Chart/Chart.js"));

        useEffect(() => {
            this.renderChart();
        });

        onPatched(() => {
            this.chart?.destroy();
            this.renderChart();
        });
        
        onWillUnmount(() => {
            this.chart?.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
        });
    }

}
