/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef, onWillUnmount } from "@odoo/owl";
import { getColor } from "@web/core/colors/colors";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        label: String,
        data: Object,
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => {
            // Load chartjs
            loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
           this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        })
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        // const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        date: data,
                        // backgroundColor: color,
                    },
                ],
            },
        });
    }
}
