import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, onWillStart, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard-item/dashboard-item"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.state = useState({ statistics: {} });
        onWillStart( async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            this.state.statistics = result;
        });
    }

    actionCustomers() {
        this.action.doAction("base.action_partner_form", { viewType: "kanban"});
    }

    actionLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
