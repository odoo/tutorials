import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./pieChart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = { title: String, data: Object };

    setup() {
        this.action = useService("action");
    }

    openOrders(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Orders (${size.toUpperCase()})`,
            res_model: "crm.lead",
            domain: [["name", "ilike", size]],
            views: [[false, "list"], [false, "form"]],
        });
    }
}
