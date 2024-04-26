/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"
import { useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { items } from "./dashboard_items";
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup(){
        this.action = useService("action")
        this.statistics= useState(useService("statisticsService"))
        this.items = items
    }

    openCustomersKanbanView(){
        this.action.doAction('base.action_partner_form')
    }
    
    openCrmLeadsView(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'CRM Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
