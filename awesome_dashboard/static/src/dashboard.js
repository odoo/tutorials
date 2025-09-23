/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout };
    static props = {};

    setup() {
        this.action = useService("action");
        this.title = "Awesome Dashboard";
    }

    openCustomers = () => {
        this.action.doAction("base.action_partner_form");
    }

    openLeads = () => {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            target: 'current',
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
