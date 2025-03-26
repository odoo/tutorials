/** @odoo-module **/

import { Component, useRef, onMounted, onPatched } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
    static template = "awesome_dashboard.piechart";

    static props = {
        orders_by_size: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.renderChart();
        });

        onPatched(() => {
            this.updateChart();
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: this.getChartData(),
        });
    }

    updateChart() {
        if (this.chart) {
            this.chart.data = this.getChartData();
            this.chart.update();
        }
    }

    getChartData() {
        return {
            labels: Object.keys(this.props.orders_by_size),
            datasets: [
                {
                    data: Object.values(this.props.orders_by_size),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#9C27B0"],
                },
            ],
        };
    }
    
}
