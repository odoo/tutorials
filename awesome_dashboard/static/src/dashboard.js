/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "@awesome_dashboard/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem };

    setup() {
        this.action = useService("action");
        this.stats = useService("awesome_dashboard_statistics");

        onWillStart(async () => {
            this.data = await this.stats.getStatistics();
        });
    }

    onClickCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            target: "current",
            res_model: "res.partner",
            views: [[false, "kanban"]],
        });
    }

    onClickLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
