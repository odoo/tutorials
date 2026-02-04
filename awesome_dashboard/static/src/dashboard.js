import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout };

    setup() {
        this.myService = useService("awesome_dashboard_service");
        this.action = useService("action");
    }

    inc() {
        this.myService.inc();
        this.render(); // simple way to refresh UI for now
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
