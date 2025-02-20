/** @odoo-module **/

import { useState, onWillStart, Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./DashboardItem/dashboard_item";

class AwesomeDashboard extends Component {
    static components = { DashboardItem, Layout };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");

        this.statistics = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            this.statistics = await this.statistics.loadStatistics();
            console.log(this.statistics);
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction("crm.crm_lead_all_leads");
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
