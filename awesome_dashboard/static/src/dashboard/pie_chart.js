import { Component, onWillStart, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useRef } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

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
        const ctx = this.canvasRef.el;

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["S", "M", "XL"],
                datasets: [{
                    data: [
                        this.props.data.s,
                        this.props.data.m,
                        this.props.data.xl,
                    ],
                }],
            },
        });
    }
}