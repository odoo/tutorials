/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/views/graph/colors";

const { Component, onWillStart, useRef, onMounted, onWillUnmount } = owl;

export class PieChart extends Component {
    setup() {
        this.canvasRef = useRef("canvas");

        this.labels = Object.keys(this.props.data);
        this.data = Object.values(this.props.data);
        this.color = this.labels.map((_, index) => {
            return getColor(index);
        });

        onWillStart(() => {
            return loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        onMounted(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.ok = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: this.labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: this.data,
                        backgroundColor: this.color,
                    },
                ],
            },
        });
    }
}

PieChart.template = "awesome_tshirt.PieChart";
