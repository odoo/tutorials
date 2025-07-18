/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "../pieChart/piechart";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };

    static props = {
        title: { type: String },
        data: { type: Object }
    }

    setup() {
        this.action = useService("action");
    }

    _t(...args) {
        return _t(...args);
    }

    onPieSliceClick(size) {
        console.log("Clicked on slice for size:", size);
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: `Orders (Size: ${size.toUpperCase()})`,
            res_model: 'sale.order',
            views: [[false, 'list'], [false, 'form']],
            domain: [["order_line.product_template_attribute_value_ids.display_name", "ilike", size]],
            target: 'current',
        });
    }
}
