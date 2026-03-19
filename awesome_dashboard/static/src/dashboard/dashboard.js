import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "./charts/pie_chart";
import { DashboardItem } from "./dashboard_items/dashboard_item";
import { NumberCard } from "./number_card/number_card";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, PieChart, DashboardItem, NumberCard };

    setup() {
        this.action = useService("action");
        this.statsService = useService("statistics");
        this.statState = useState(this.statsService.state);
        console.log(this.statState, "STSTST");
    }
    openSettings() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.config.settings",
            views: [[false, "form"]],
        });
    }
    viewCustomers() {
        this.action.doAction({
            name: _t("Customers"),
            type: "ir.actions.act_window",
            res_model: "res.partner",
            views: [[false, "kanban"]],
        });
    }
    viewLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            target: "current",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
