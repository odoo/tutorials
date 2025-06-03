/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: {
            type: Object,
            optional: true,
            default: null,
        },
    }

    setup() {
        this.chart = null;

        this.rootRef = useRef("root");
        this.canvasRef = useRef("canvas");
        this.containerRef = useRef("container");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        useEffect(() => this.renderChart());
    }

    generateData() {
        if (this.props.data === null || Object.keys(this.props.data).length === 0)
            return {};

        const labels = Object.keys(this.props.data);
        const datasets = [];

        datasets.push({
            label: 'Shirt Sizes',
            data: Object.values(this.props.data),
            backgroundColor: [
                'rgba(27, 192, 204, 0.2)',
                'rgba(207, 116, 30, 0.2)',
                'rgba(255, 206, 86, 0.2)',
            ],
        });

        return { labels, datasets };
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = {
            type: 'pie',
            data: this.generateData(),
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Shirt Order By Size'
                    }
                }
            },
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
