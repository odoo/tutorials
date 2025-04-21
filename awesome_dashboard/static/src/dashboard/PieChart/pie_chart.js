/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        label: { type: String },
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
    }

    getChartConfig() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        return {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: ['#FFD86D', '#43C5B1', '#4EA7F2'],
                    },
                ],
            },
        };
    }

    onSliceClick(size) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Orders with size ' + size,
            res_model: 'sale.order',
            domain: [['size', '=', size]],
            views: [[false, "list"]],
            target: "current",
        });
    }
}
