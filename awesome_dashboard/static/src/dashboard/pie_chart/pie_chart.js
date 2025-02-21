import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";

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
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        console.log(data)
        this.chart = new Chart(this.canvasRef.el, {

            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: ['#ff5733', '#ff8d1a', '#ffcc00'],    
                    },
                ],
            },
            options: {
                plugins: {
                    legend: {
                        labels: {
                            color: "#FFF",
                            font: {
                                size: 14,
                                weight: "bold",
                            },
                        },
                    },
                },
            },
        });
    }
}
