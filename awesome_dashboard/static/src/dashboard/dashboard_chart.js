import { Component, onWillStart, useRef, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class DashboardChart extends Component {
    static template = "awesome_dashboard.DashboardChart"
    static props = {
        label: String,
        data: Object,
        type: { validate: t => ["pie", "bar", "line"].includes(t) },
    }

    setup() {
        this.canvasRef = useRef('canvas')
        onWillStart(() => {
            return loadJS("/web/static/lib/Chart/Chart.js")
        })
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            this.chart?.destroy();
        })
    }

    renderChart() {
        this.chart?.destroy();
        const config = {
            type: this.props.type,
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: this.props.label,
                    data: Object.values(this.props.data)

                }],
            }

        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
