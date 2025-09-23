import { loadJS } from "@web/core/assets";
import { Component, onWillStart, useRef, useEffect, onWillUnmount } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            if (this.chart) { this.chart.destroy();} 
            this.displayChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    displayChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                    },
                ],
            },
        });
    }
}