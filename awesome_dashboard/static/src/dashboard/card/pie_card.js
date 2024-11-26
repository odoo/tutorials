/** @odoo-module **/

import {Component, onMounted, onWillStart, onWillUnmount, onWillUpdateProps, useRef} from "@odoo/owl";
import {loadJS} from "@web/core/assets";


export class PieCard extends Component {
    static template = "awesome_dashboard.PieCard";

    static props = {
        title: {type: String},
        value: {type: Object},
    }

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => {
            this.renderChart();
        });

        onWillUpdateProps(() => {
            // Refresh the chart whenever the props are updated
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

        const labels = Object.keys(this.props.value);
        const colors = labels.map((label, idx) => {
            return this.getColor(idx)
        })

        const config = {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.title,
                        data: Object.values(this.props.value),
                        backgroundColor: colors,
                    },
                ],
            },
        }
        this.chart = new Chart(this.canvasRef.el, config);
    }

    getColor(index) {
        return COLORS[index % COLORS.length];
    }

}

export const COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#aec7e8",
    "#ffbb78",
    "#2ca02c",
    "#98df8a",
    "#d62728",
    "#ff9896",
    "#9467bd",
    "#c5b0d5",
    "#8c564b",
    "#c49c94",
    "#e377c2",
    "#f7b6d2",
    "#7f7f7f",
    "#c7c7c7",
    "#bcbd22",
    "#dbdb8d",
    "#17becf",
    "#9edae5",
];

