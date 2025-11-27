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

    openOrders(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders with size %s", size),
            res_model: "awesome_dashboard.order", // Assuming a model exists or generic search
            domain: [["size", "=", size]],
            views: [[false, "list"], [false, "form"]],
        });
    }
}
