/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        stats_data: { type: Object },
       };
    
    setup() {
        this.action = useService("action");
        this.canvasRef = useRef("canvas");
        this.chart = null;
        onWillStart(async () =>
            await loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            this.renderChart();
        });
    }

    displayPieChartInfo(id) {
        return this.action.doAction({
            res_model: "sale.order",
            name: "T-shirts",
            type: "ir.actions.act_window",
            views: [[false, "tree"]],
            view_mode: "tree",
            //domain: [['order_line.product_id', '=', 'id']],
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                datasets: [{
                    data: Object.values(this.props.stats_data)
                }],
                labels: Object.keys(this.props.stats_data)
            },
            options: {
                onClick: (e, temp) => {
                    this.displayPieChartInfo(temp);
                }
            }
        });
    }
}