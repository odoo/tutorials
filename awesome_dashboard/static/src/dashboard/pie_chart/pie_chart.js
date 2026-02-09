import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        label: this.props.label,
                        data: Object.values(this.props.data),
                    },
                ],
            },
        });
    }
}
