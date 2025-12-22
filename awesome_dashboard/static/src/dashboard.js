import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component } from "@odoo/owl";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout };

    setup() {
        this.action = useService("action");
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
