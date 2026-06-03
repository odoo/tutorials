import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
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
            const ctx = this.canvasRef.el.getContext("2d");

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [{
                        data: Object.values(this.props.data),
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });
        });
    }
}
