/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: {
            type: Object
        }
    }

    setup() {
        this.canvasRef = useRef("canvas");


        onWillStart(
            () => loadJS(["/web/static/lib/Chart/Chart.js"])
        );

        useEffect(
            () => {
                this.renderChart();
            },
            () => []
        );

        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    getChartConfig() {
        let config = {};
        config.type = "pie";
        config.data = this.props.data;
        return config;
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        let config = this.getChartConfig();
        this.chart = new Chart(this.canvasRef.el, config);
        console.log(config)
    }

}
