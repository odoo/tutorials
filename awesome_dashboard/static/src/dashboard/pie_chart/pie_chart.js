import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
        onWillUnmount(() => this.chart?.destroy());
    }

    renderChart() {
        this.chart?.destroy();
        const ctx = this.canvasRef.el;
        this.chart = new Chart(ctx, {
            type: "doughnut",
            data: {
                datasets: [{ data: Object.values(this.props.data) }],
                labels: Object.keys(this.props.data),
            },
        });
    }
}
