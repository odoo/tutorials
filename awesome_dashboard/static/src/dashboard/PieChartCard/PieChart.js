import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = { data: Object };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("chartCanvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            if (this.chart) {
                this.chart.destroy();
            }
            if (!this.props.data) {
                console.warn("No data available for PieChart");
                return;
            }

            const ctx = this.canvasRef.el.getContext("2d");

            this.chart = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data), // Labels from API (S, M, L, XL, XXL)
                    datasets: [{
                        label: "T-Shirts Sold",
                        data: Object.values(this.props.data), // Extracts numeric values
                        backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
                    }]
                }
            });
        })
    }
}
