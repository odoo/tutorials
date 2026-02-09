/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvasRef = useRef("canvas");

        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");

            const canvas = this.canvasRef.el;
            const ctx = canvas.getContext("2d");

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: ["m", "s", "xl"],
                    datasets: [{
                        data: [30, 10, 5]
                    }]
                }
            });
        });
    }
}
