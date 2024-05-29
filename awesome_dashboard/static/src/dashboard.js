/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dasboard_item"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            this.stats = await this.statistics.loadStatistics();
        });
    }
    showCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'tree'], [false, 'form']],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
