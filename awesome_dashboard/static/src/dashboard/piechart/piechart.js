import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart"

    setup() {
        this.canvasRef = useRef("canvas")
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
    }
    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        const data = this.props.data || {};
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["S", "M", "XL"],
                datasets: [
                    {
                        data: [
                            data.s || 0,
                            data.m || 0,
                            data.xl || 0,
                        ],
                    },
                ],
            },
        });
    }
}
