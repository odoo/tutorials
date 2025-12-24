import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object },
    };
    setup(){
        this.canvasRef = useRef("canvas");
        onWillStart(async() => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
    }
    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["S", "M", "L", "XL", "XXL"],
                datasets: [
                    {
                        data: [
                            this.props.data.s || 2,
                            this.props.data.m || 5,
                            this.props.data.l || 7,
                            this.props.data.xl || 11,
                            this.props.data.xxl || 13,
                        ],
                        backgroundColor: [
                            "#ff6384",
                            "#36a2eb",
                            "#ffce56",
                            "#4bc0c0",
                            "#9966ff",
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            },
        });
    }
}