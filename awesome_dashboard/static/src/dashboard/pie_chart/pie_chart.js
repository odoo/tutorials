/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.action = useService("action");
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]))
        useEffect(() => this.createPieChart());
        onWillUnmount(() => {
            this.chart.destroy();
        })
    }

    formatPieData() {
        const pieData = {
            datasets: [{ data: [] }],
            labels: []
        };

        for (const size in this.props.data) {
            pieData.datasets[0].data.push(this.props.data[size])
            pieData.labels.push(size)

        }

        return pieData
    }

    showOrders() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("T-Shirt orders"),
            target: "current",
            res_model: "sale.order",
            views: [
                [false, "list"],
            ],
        });
    }

    createPieChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: this.formatPieData(),
            options: {
                onClick: (e, arr) => this.showOrders() 
            }
        })
    }

}
