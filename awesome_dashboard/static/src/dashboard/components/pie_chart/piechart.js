import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";

    static props = {
        // The labels array e.g. ["S", "M", "L", "XL"]
        labels: { type: Array },
        // The values array e.g. [10, 20, 30, 40]
        values: { type: Array },
        title: { type: String, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas2");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        useEffect(
            () => this.renderChart(),
            () => [this.props.labels, this.props.values]
        );

        onWillUnmount(() => this.destroyChart());
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        if (this.chart) {

            this.chart.data.labels = this.props.labels;
            this.chart.data.datasets[0].data = this.props.values;
            this.chart.update();
            return;
        }


        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: this.props.labels,
                datasets: [{ data: this.props.values }],
            },
        });
    }
}