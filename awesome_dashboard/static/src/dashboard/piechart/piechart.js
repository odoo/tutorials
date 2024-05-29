/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadBundle, loadJS } from "@web/core/assets";

export class PieChart extends Component {
    setup() {
        this.chart = undefined;
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
        });

        useEffect(() => {
            this.renderChart();
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            };
        });
    }

    getChartData() {
        return {
            type: "pie",
            data: {
                labels: ["S", "M", "L"],
                datasets: [
                    {
                        data: [this.props.data.s, this.props.data.m, this.props.data.l],
                        backgroundColor: ["#ff7200", "#36A2EB", "#80b9e5"],
                        hoverBackgroundColor: ["#ff7200", "#36A2EB", "#80b9e5"],
                    },
                ],
            }
        }
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, this.getChartData());
    }
}

PieChart.template = "awesome_dashboard.PieChart";
PieChart.props = {
    data: { type: Object },
}