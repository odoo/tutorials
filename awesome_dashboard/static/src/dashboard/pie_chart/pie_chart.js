import { Component, onWillStart, onWillUnmount, useRef, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";

    static props = {
        title: { type: String },
        value: {
            type: Object,
            shape: {
                m: Number,
                s: Number,
                xl: Number
            }
        },
    }

    setup() {
        this.action = useService("action");
        this.canvasRef = useRef('canvas');
        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"])
        });
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getChartConfig());
    }

    getChartConfig() {
        const data = [this.props.value.m, this.props.value.s, this.props.value.xl]
        return {
            type: 'pie',
            data: {
                labels: ['m', 's', 'xl'],
                datasets: [{
                    label: 'Total Orders',
                    data: data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        };
    }
}
