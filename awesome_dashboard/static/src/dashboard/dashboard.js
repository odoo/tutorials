/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { items } from "./dashboard_items";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup(){
        this.action = useService("action");
        const statistics = useService("stats");
        this.stats = useState(statistics.loadStatistics());
        this.items = items
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
        type: 'ir.actions.act_window',
        name: 'Leads',
        res_model: 'crm.lead',
        views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
