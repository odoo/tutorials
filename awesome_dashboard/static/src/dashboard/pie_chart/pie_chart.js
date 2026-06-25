import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadBundle } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
        onSliceClick: { type: Function, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
        });

        useEffect(() => {
            this.renderChart();
        });

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
        const data = this.props.data;
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(data).map((k) => k.toUpperCase()),
                datasets: [
                    {
                        data: Object.values(data),
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }

    handleClick(event) {
        if (!this.chart || !this.props.onSliceClick) {
            return;
        }
        const canvas = this.canvasRef.el;
        const rect = canvas.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const clickY = event.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const distance = Math.hypot(clickX - centerX, clickY - centerY);
        const radius = Math.min(rect.width, rect.height) / 2;
        if (distance > radius) {
            return;
        }

        const data = this.props.data;
        const keys = Object.keys(data);
        const values = Object.values(data);
        const total = values.reduce((sum, value) => sum + value, 0);
        if (!total) {
            return;
        }

        const angle = Math.atan2(clickY - centerY, clickX - centerX);
        const normalizedAngle = (angle - (-Math.PI / 2) + 2 * Math.PI) % (2 * Math.PI);

        let accumulatedAngle = 0;
        for (let index = 0; index < values.length; index++) {
            accumulatedAngle += (values[index] / total) * 2 * Math.PI;
            if (normalizedAngle <= accumulatedAngle || index === values.length - 1) {
                this.props.onSliceClick(keys[index]);
                return;
            }
        }
    }
}
