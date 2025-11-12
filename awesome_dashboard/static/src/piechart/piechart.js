/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart"
    static props = {
        data: {
            stats: Object
        }
    }

    canvasRef = useRef("canvas");
    pieChart = null;

    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            if (this.pieChart) {
                this.pieChart.destroy();
            }
        });
    }

    renderChart() {
        if (this.pieChart) this.pieChart.destroy()
        this.pieChart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props),
                datasets: [{ data: Object.values(this.props) }]
            },
            options: {
                onClick: (e,arr) => {
                    const clickedElement = arr[0];
                    const datasetIndex = clickedElement.index;
                    const labelValue = Object.values(this.props)[datasetIndex];
                    console.log(labelValue)
                }
            }
        })
    }
}
