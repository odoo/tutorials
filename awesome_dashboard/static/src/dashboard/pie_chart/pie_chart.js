/** @odoo-module **/

import { Component, onWillStart, useRef, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
    static template = "awesome_dashboard.PieChart";
    static props = {
       data: { type: Object, optional: false }
    }

    setup(){
        this.data = this.props.data;
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))

        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart(){
        if(this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.data),
                datasets: [
                    {
                        label: "T-Shirts Sold by Size",
                        data: Object.values(this.data),
                        backgroundColor: 
                        [
                            "#007bff",
                            "#28a745",
                            "#ffc107"
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });
    }
}
