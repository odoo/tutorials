
import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };
    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
    }
    renderChart() {
        if (!this.props.data) {
            return;
        }
        const ctx = this.canvasRef.el.getContext("2d");
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["S", "M", "L", "XL", "XXL"],
                datasets: [{
                    data: [
                        this.props.data.s || 0,
                        this.props.data.m || 0,
                        this.props.data.l || 0,
                        this.props.data.xl || 0,
                        this.props.data.xxl || 0,
                    ],
                }],
            },
        });
    }
}
