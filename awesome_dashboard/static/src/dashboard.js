/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };
    static props = {};

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.title = "Awesome Dashboard";

        onWillStart(async () => {
            this.statistics = await this.statisticsService.loadStatistics();
        });
        console.log(this.statistics)
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
