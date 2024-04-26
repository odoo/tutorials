/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object
    }

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        this.action = useService("action");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    showOrders(index) {
        console.log(index)
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('T-Shirts'),
            res_model: 'sale.order',
            views: [[false, 'tree']],
            domain: "[('order_line.product_id.product_tmpl_id.id', '=', '30')]"
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const data = {
            labels: Object.keys(this.props.data).map(label => label.toUpperCase()),
            datasets: [{
                label: _t("# of Orders"),
                data: Object.values(this.props.data)
            }]
        }
        const options = {
            events: ['click'],
            onClick: (_ev, arr) => this.showOrders(arr[0].index)
        }
        this.chart = new Chart(this.canvasRef.el, {data, options, type: "pie"});
    }
}