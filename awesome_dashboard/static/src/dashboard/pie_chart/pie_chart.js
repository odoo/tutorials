/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

import { DashboardItem } from "../dashboard_item/dashboard_item.js";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object
    };

    setup() {
        this.chartItemCanvasRef = useRef("chartItemCanvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }
    
    renderChart() {
        /*
        this.chart = new Chart(this.chartItemCanvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        label: "orders_by_size",
                        data: Object.values(this.props.data),
                    },
                ],
            },
        });
        */
    }

    static components = { DashboardItem };
}