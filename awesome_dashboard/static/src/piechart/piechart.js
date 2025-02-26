/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvasref");
        onWillStart(async () => await loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
    }

    static props = {
        data: { type: Object },
        title: { type: String, optional: true },
        responsive: { type: Boolean, optional: true }
    }

    static defaultProps = {
        responsive: true,
        title: ""
    };


    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getPieChartConfig())
    }

    getPieChartConfig() {
        const pieData = {
            labels: Object.keys(this.props.data),
            datasets: [
                {
                    data: Object.values(this.props.data),
                }
            ]
        }
        const config = {
            type: 'pie',
            data: pieData,
            options: {
                responsive: this.props.responsive,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: this.props.title
                    }
                }
            }
        };
        return config
    }
}
