import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(async () => await loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            this.renderChart();
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            };
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        const config = {
            type: "pie",
            data: this.props,
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
