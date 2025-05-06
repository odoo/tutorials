import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: String,
        values: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    };

    renderChart() {
        this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.values),
                    datasets: [{
                        data: Object.values(this.props.values),
                        backgroundColor: ["green", "blue", "orange", "red", "purple"],
                        hoverOffset: 3
                    }],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                        title: {
                            display: true,
                            text: this.props.title,
                        }
                    }
                }
            }
        )
    };
}
