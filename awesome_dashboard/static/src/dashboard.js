import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout };

    setup() {
        this.action = useService("action");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
