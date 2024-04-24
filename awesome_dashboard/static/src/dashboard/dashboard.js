/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
        this.action = useService("action");
        this.statsService = useService("awesome_dashboard.statistics");
        this.stats_proxy = useState(this.statsService.statistics);
    }

    showCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'tree'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard", AwesomeDashboard);
