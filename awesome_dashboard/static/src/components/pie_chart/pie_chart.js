import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChartTemplate";
    static props = {
        tshirtSales: Object,
    };

    setup() {
        this.canvasRef = useRef("chartCanvas");

        onWillStart(() =>loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(()=> {
            this.renderChart();
        })
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.tshirtSales),
                datasets: [{
                    data: Object.values(this.props.tshirtSales),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}
