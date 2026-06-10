import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        data: Object,
        title: { type: String, optional: true },
    };

    setup() {
        this.action = useService("action");
    }

    openOrdersBySize(size) {
        return this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Sales Orders"),
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            view_mode: "list,form",
            target: "current",
            domain: [["order_line.product_template_attribute_value_ids.name", "ilike", size]],
        });
    }
}
