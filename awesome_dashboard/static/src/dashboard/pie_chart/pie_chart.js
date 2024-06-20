/** @odoo-module **/

import { Component, onWillStart, useRef, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(
            () => {
                this.renderChart();
            },
            () => [this.props.data]
        );
        onWillUnmount(() => this.chart.destroy());
    }

    async renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
            options: {
                aspectRatio: 2,
                onClick: (evt, el) => {
                    let point = this.chart.getElementsAtEventForMode(
                        evt,
                        "point",
                        {
                            intersect: true,
                        },
                        true
                    );
                    const label = this.chart.data.labels[point[0].index];
                    const quantity = this.chart.data.datasets[point[0].datasetIndex].data[point[0].index];
                    alert(`Opening: ${label} (${quantity})`);
                    console.log(
                        "Mode point list: ",
                        this.chart.data.labels[point[0].index], // Label
                        this.chart.data.datasets[point[0].datasetIndex].data[point[0].index] // Value
                    );
                },
            },
        });
    }
}
