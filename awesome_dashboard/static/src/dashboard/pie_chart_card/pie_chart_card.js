import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static props = {
        data: { type: Object },
        title: { type: String },
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.drawChart();
        });
    }

    drawChart() {
        new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        label: this.props.title,
                        data: Object.values(this.props.data),
                    },
                ],
            },
        });
    }
}
