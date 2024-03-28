/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, onMounted, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        const canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onWillUnmount(() => {
            this.chart?.destroy();
        });

        onMounted(() => {
            const data = this.props.data;

            this.chart = new Chart(canvasRef.el, {
                type: "pie",
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        data: Object.values(data),
                    }],
                },
            });
        });

        useEffect(() => {
            const data = this.props.data;
            this.chart.data.datasets[0].data = Object.values(data);
            this.chart.update();
        });
    }
}
