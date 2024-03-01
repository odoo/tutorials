/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        //this.openSettings = this.openSettings.bind(this);
    }
    openCustomerList() {
        console.log('clicked');
        this.action.doAction("base.action_partner_form");
    }
    openLeadList() {
        console.log('clicked');
        this.action.doAction("crm.crm_lead_all_leads");
    }

    static components = { Layout };
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
