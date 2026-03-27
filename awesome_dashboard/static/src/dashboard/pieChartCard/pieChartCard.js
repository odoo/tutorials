import { Component } from "@odoo/owl";
import { PieChart } from "../pieChart/pieChart";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.pieChartCard";

    static components = { PieChart };

    static props = {
        title: { type: String },
        values: { type: Object },
    };

    setup() {
        this.action = useService("action");
    }

    onSelectLabel(label) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t("Orders with size %s", [label]),
            res_model: 'awesome_dashboard.orders',
            domain: [['size', '=', label]],
            views: [[false, 'list']],
            target: 'current',
        });
    }
}
