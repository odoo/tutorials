/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, onWillUpdateProps } from "@odoo/owl"
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: { type: Object, optional: false },
    };

    setup() {
        this.canvasRef = useRef("canvas")

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")
        });

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

    renderChart(data = this.props.data) {
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["M", "S", "XL"],
                datasets: [
                    {
                        data: [
                            data.m || 0,
                            data.s || 0,
                            data.xl || 0,
                        ],
                        backgroundColor: ["#007BFF", "#FFA500", "#808090",]
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            },
        });
    }
}
