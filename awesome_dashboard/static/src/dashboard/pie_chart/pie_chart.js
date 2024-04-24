/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object
    }

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

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
        const data = {
            labels: Object.keys(this.props.data).map(label => label.toUpperCase()),
            datasets: [{
                label: "# of Orders",
                data: Object.values(this.props.data)
            }]
        }
        this.chart = new Chart(this.canvasRef.el, {data: data, options: {}, type: "pie"});
    }
}