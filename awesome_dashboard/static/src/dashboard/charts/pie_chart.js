/** @odoo-module */

import { Component, onWillStart, useEffect, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            this.chart.destroy();
            
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
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
                        backgroundColor: color
                    }
                ]
            }
        });
    }
}
