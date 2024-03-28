/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, onMounted, useEffect, useRef } from "@odoo/owl";
import { getColor } from "@web/core/colors/colors";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        label: { type: String },
        data: { type: Object }
    };

    setup(){

        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        onMounted(() => this.renderChart());

        onWillUnmount(() => {
            this.chart.destroy();
        });

        useEffect(() => {
            const data = this.props.data;
            this.chart.data.datasets[0].data = Object.values(data);
            this.chart.update();
        });

    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
        });
    }
}
