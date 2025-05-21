/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object },
        options: { type: Object, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        if (this.canvasRef.el) {
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: this.props.data,
                options: this.props.options,
            });
        }
    }
}
