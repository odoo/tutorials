/** @odoo-module **/

import { Component, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;   // store chart instance

        const renderChart = async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");

            const canvas = this.canvasRef.el;
            if (!canvas) return;

            const dataObj = this.props.data || {};
            const sizes = Object.keys(dataObj);
            const quantities = Object.values(dataObj);

            // If chart already exists → update it
            if (this.chart) {
                this.chart.data.labels = sizes.map(s => s.toUpperCase());
                this.chart.data.datasets[0].data = quantities;
                this.chart.update();
                return;
            }

            // Otherwise create new chart
            const ctx = canvas.getContext("2d");
            this.chart = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: sizes.map(s => s.toUpperCase()),
                    datasets: [{
                        data: quantities,
                    }]
                },
                options: {
                    onClick: (evt, elements) => {
                        if (!elements.length) return;
                        const idx = elements[0].index;
                        const size = this.chart.data.labels[idx].toLowerCase(); // "M" -> "m"
                        this.props.onSliceClick?.(size);
                    }
                }
            });
        };

        // First render
        onMounted(() => {
            renderChart();
        });

        // Re-run when props.data changes
        useEffect(
            () => {
                renderChart();
            },
            () => [this.props.data]
        );

        // Cleanup
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        });
    }
}
