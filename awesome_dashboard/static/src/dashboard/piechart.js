import { Component, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        sizes: Array,        // Labels (e.g., ["S", "M", "L"])
        quantities: Array,   // Data values (e.g., [10, 20, 30])
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");

            if (!this.canvasRef.el) return;  // Ensure the canvas exists

            const ctx = this.canvasRef.el.getContext("2d");
            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: this.props.sizes,
                    datasets: [{
                        data: this.props.quantities,
                        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#9C27B0"],
                    }],
                },
            });
        });
    }
}
