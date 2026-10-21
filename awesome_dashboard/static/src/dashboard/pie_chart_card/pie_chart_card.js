import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: String,
        values: Object,
    };

    setup() {
        this.action = useService("action");
    }

    openOrdersBySize(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders by size"),
            res_model: "sale.order",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [["order_line.product_id.product_template_attribute_value_ids.name", "=ilike", size]],
        });
    }
}
