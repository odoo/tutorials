/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./dashboard_item.js"


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
    }

    viewCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    viewLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    static components = { Layout, DashboardItem };
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
