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
                            this.props.data.s || 11,
                            this.props.data.m || 9,
                            this.props.data.l || 13,
                            this.props.data.xl || 7,
                            this.props.data.xxl || 15,
                        ],
                        backgroundColor: [
                            "#ff6384",
                            "#36a2eb",
                            "#ffce56",
                            "#4bc0c0",
                            "#906fd1",
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
