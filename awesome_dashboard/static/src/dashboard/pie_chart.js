/** @odoo-module **/

import { Component, onWillStart, onMounted, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static props = {sizes: {type: Object}}
    static template = "awesome_dashboard.pie_chart";

    setup() {
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onWillUpdateProps((props) => {
            this.chart.destroy();
            this.renderChart(props);
        });

        onMounted(() => {
            this.renderChart(this.props);
        });
    }

    renderChart(props) {
            const ctx = document.getElementById('myChart');
            const sizeData = props.sizes; // Assumes response like { sizes: { S: 100, M: 80, ... } }
            const labels = Object.keys(sizeData);
            const data = Object.values(sizeData);

            this.chart = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"
                        ],
                    }],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "bottom",
                        },
                        title: {
                            display: true,
                            text: "T-Shirt Sizes Sold",
                        },
                    },
                },
            });
        }

}