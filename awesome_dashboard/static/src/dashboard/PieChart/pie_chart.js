/** @odoo-module **/
import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    setup() {
        this.canvasRef = useRef("chartCanvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            if (!this.props.data || Object.keys(this.props.data).length === 0) {
                return;
            }

            const ctx = this.canvasRef.el.getContext("2d");
            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data), // ['m', 's', 'xl']
                    datasets: [
                        {
                            label: "T-Shirt Sales",
                            data: Object.values(this.props.data), // [22, 68, 41]
                            backgroundColor: [
                                "#FF6384", // Red
                                "#36A2EB", // Blue
                                "#FFCE56", // Yellow
                            ],
                            hoverOffset: 22
                        },
                    ],
                },
            });
        });
    }
}

PieChart.template = "awesome_dashboard.PieChart";
PieChart.props = {
    data: Object,
};
