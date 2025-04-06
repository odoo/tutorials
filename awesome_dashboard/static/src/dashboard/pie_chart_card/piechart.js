import { Component, useRef, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

// PieChart component for visualizing data in a pie chart
export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static components = [];
    static props = {
        data: Object, // Data to be visualized
    };

    setup() {
        // Load the Chart.js library before the component starts
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        // Reference to the canvas element where the chart will be rendered
        this.canvasRef = useRef("canvas");

        // Render the chart once the component is mounted
        onMounted(() => {
            this.renderChart();
        });

        // Clean up and destroy the chart when the component is unmounted
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    // Function to render the pie chart using Chart.js
    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
        });
    }
}
