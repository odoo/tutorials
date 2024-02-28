/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { required: true, },
    };

    setup() {
        this.canvasRef = useRef("canvas");


        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        useEffect(() => {
            this.destroyChart();

            this.chart = new Chart(this.canvasRef.el, {
                type: 'pie',
                data: this.props.data,
            });
        });

        onWillUnmount(this.destroyChart);
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}
