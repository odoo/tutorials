import { _t } from "@web/core/l10n/translation";
import { Component, onWillStart, useEffect, onWillUnmount, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.action = useService("action");
        this.canvasRef = useRef('canvas');
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => this.renderChart());
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    /**
     * Creates and binds the chart on `canvasRef`.
     */
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext('2d');
        this.chart = new Chart(ctx, this.getChartConfig());
    }

    onGraphClicked(ev) {
        const points = this.chart.getElementsAtEventForMode(ev, 'nearest', { intersect: true }, false);

        if (points.length) {
            const index = points[0].index;
            const label = this.chart.data.labels[index];

            this.action.doAction({
                type: 'ir.actions.act_window',
                name: _t('Sales'),
                res_model: 'sale.order',
                views: [[false, 'list'], [false, 'form']],
                target: 'current',
                domain: [['order_line.product_id', 'ilike', '' + label]]
            })
        }
    }

    /**
     * @returns {object} Chart config for the current data
     */
    getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data)
                }]
            },
            options: {
                onClick: this.onGraphClicked.bind(this)
            }
        };
    }
}
