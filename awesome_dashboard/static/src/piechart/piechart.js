import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        items: {
            type: Object,
            optional: true,
            default: { m: 0, s: 0, xl: 0 },
        },
    };

    setup() {
        this.chartRef = useRef("pie-canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");

            this.pieChartData = {
                labels: ["M", "S", "XL"],
                datasets: [
                    {
                        label: "Sales Count",
                        data: [
                            this.props.items.m ?? 0,
                            this.props.items.s ?? 0,
                            this.props.items.xl ?? 0,
                        ],
                    },
                ],
            };

            this.pieChartOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "top" } },
            };
        });

        onMounted(() => {
            const canvasEl = this.chartRef.el;
            if (!canvasEl) {
                return;
            }
            const ctx = canvasEl.getContext("2d");
            if (!ctx || !window.Chart) {
                return;
            }
            this.myPie = new window.Chart(ctx, {
                type: "pie",
                data: this.pieChartData,
                options: this.pieChartOptions,
            });
        });
    }
}
