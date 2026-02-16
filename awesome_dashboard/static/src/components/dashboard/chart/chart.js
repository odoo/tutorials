import { Component, useRef, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class DashboardChart extends Component {
    static template = "awesome_dashboard.DashboardChart";
    static props = {
        label: { type: String, optional: true, default: "Dataset" },
        data: { type: Object, required: true },
    };
    setup() {
        this.chartRef = useRef("DashboardChart");
        onWillStart(async () => {
            // Ensure Chart.js library is loaded before we try to use it
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            // The canvas now exists in the DOM
            this.renderChart();
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.chartRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                    },],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // <--- Add this line
            }
        });
        console.log("Chart rendered with data:", this.chartRef.el);
    }



}
