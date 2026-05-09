import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("chart");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data),
                }],
            },
        });
    }
}
