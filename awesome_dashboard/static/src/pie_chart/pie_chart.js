import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        title: { type: String },
        value: { type: Object },
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(
            () => {
                this.createChart();
                return () => this.chart?.destroy();
            },
            () => [this.props.value]
        );
    }

    getChartConfig() {
        if (!this.props.value) {
            return null;
        }

        return {
            type: "pie",
            data: {
                labels: Object.keys(this.props.value),
                datasets: [
                    {
                        data: Object.values(this.props.value),
                    },
                ],
            },
        };
    }

    createChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        const config = this.getChartConfig();
        if (config) {
            this.chart = new Chart(this.canvasRef.el, config);
        }
    }
}
