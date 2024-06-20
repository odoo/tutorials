/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./dashboard_item.js"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");

        onWillStart(async () => { this.statistics = await this.statistics.loadStatistics(); })
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
