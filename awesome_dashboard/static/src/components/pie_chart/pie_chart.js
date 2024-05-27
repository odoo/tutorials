/** @odoo-module **/

import { Component, onWillDestroy, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadBundle } from "@web/core/assets";

export class PieChart extends Component {
    static template = 'awesome_dashboard.pie_chart';
    static props = {
        data: { type: Object },
        options: { type: Object, optional: true },
    };

    setup() {
        this.canvasRef = useRef('pie-canvas');

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
        });
        useEffect(() => this.renderChart());
        onWillDestroy(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const config = {
            type: 'pie',
            data: this.props.data,
            options: this.props.options,
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
