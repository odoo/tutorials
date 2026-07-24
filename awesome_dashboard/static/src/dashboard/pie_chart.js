import { Component, onWillStart, useEffect, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        // ERROR; Redirection through props/useState fails meta-function application!
        // eg this.props.stats.keys() won't return what you think!
        stats: {
            type: Object,
            shape: {
                m: Number,
                s: Number,
                xl: Number,
            }
        },
        slots: { type: Object, optional: true },
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            // Injects the script directly into the frontend
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    getChartConfig() {
        const stats = this.props.stats;
        console.log(stats);
        return {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [stats.m, stats.s, stats.xl],
                }],
                labels: ["m", "s", "xl"],
            },
            options: {},
        };
    }

    // NOTE; Ripped from https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/addons/web/static/src/views/graph/graph_renderer.js#L618
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
        // To perform its animations, ChartJS will perform each animation
        // step in the next animation frame. The initial rendering itself
        // is delayed for consistency. We can avoid this by manually
        // advancing the animation service.
        // (?) Chart.animationService.advance();
    }
}