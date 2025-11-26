/** @odoo-module **/

import { Component, onMounted, useRef, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        sizes: Array,
        quantities: Array,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null; 

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart(this.props.sizes, this.props.quantities);
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.destroy();
            }
            this.renderChart(nextProps.sizes, nextProps.quantities);
        });
    }

    renderChart(sizes, quantities) {
        if (!this.canvasRef.el) return;

        const ctx = this.canvasRef.el.getContext("2d");

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: sizes,
                datasets: [{
                    data: quantities,
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#9C27B0"],
                }],
            },
        });
    }
}
