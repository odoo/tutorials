/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        this.statisticService = useService("statisticService");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        useEffect(() => {
            this.renderChart();
        });
    }

    /**
     * Instantiates a Chart (Chart.js lib) to render the graph according to
     * the current config.
     */
    async renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        // FIXME: directly use this.props.data object instead of extracting labels and data
        const labels = Object.keys(this.props.data.orders_by_size);
        const data = Object.values(this.props.data.orders_by_size);

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
            },
        });
    }
}
