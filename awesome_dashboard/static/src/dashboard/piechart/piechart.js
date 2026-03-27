/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    
    setup() {
        this.canvasRef = useRef("canvas");


        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
    const canvas = this.canvasRef.el;

    if (!canvas) {
        console.error("Canvas not found error");
        return;
    }

    const ctx = canvas.getContext("2d");

    const data = this.props.data || {};
    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [
                {
                    data: values,
                },
            ],
        },
    });
}
}