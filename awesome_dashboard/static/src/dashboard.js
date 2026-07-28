import { Component, useSubEnv, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { DashboardItem } from "./dashboard_item/dashboard_item";

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

        this.action = useService("action");
        this.display = { controlPanel: {} };

        this.stats = useState({ data: {} });
        onWillStart(async () => {
            this.stats.data = await rpc("/awesome_dashboard/statistics");
        });
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

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
