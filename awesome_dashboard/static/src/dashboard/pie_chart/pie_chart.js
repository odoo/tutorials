import { Component, onWillStart, onMounted, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = 'awesome_dashboard.PieChart';
    static props = {
        data: Object,
    };

    setup() {
        const canvasRef = useRef('canvas');

        onWillStart(async () => {
            await loadJS('/web/static/lib/Chart/Chart.js');
        });

        onMounted(() => {
            const canvas = canvasRef.el;
            const ctx = canvas.getContext('2d');
            this.chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [
                        {
                            data: Object.values(this.props.data),
                        },
                    ],
                },
                options: {},
            });
            this.chart.update();
        });

        useEffect(
            data => {
                this.chart.data.labels = Object.keys(data);
                this.chart.data.datasets[0].data = Object.values(data);
                this.chart.update();
            },
            () => [this.props.data],
        );

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
}
