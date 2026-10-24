import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout};

    setup() {
        this.action = useService("action");
    }

    openCustomers() {

        this.action.doAction("res.partner.action_partner_kanban");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "kanban"], [false, "form"]],
            target: "current",
        });
    }
    
    openCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            res_model: "res.partner",
            views: [[false, "kanban"], [false, "form"]],
            target: "current",
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
