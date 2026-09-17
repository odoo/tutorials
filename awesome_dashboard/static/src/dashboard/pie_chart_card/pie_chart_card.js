import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: String,
        data: Object,
    };

    setup() {
        this.action = useService("action");
    }

    onPieClick(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Shirt Orders (%s)", size),
            res_model: "res.partner",
            domain: [["name", "ilike", size]],
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}
