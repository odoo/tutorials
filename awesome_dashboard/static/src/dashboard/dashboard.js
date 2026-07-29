import { Component, useSubEnv, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { items } from "./dashboard_items";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };
    static props = { "*": true };

    setup() {
        useSubEnv({
            config: {
                ...this.env.config,
                breadcrumbs: [{ name: "Dashboard" }],
            },
        });

        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = items;
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
