/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"
import { useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { PieChart } from "./pie_chart/pie_chart"; 
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup(){
        this.statisticsDescription = {
            'average_quantity':'Average amount of t-shirt by order this month',
            'average_time':'Average time for an order to get from "new" to "sold" or "canceled"',
            'nb_new_orders':'Number of new orders this month',
            'nb_cancelled_orders':'Number of canceled orders this month',
            'total_amount':'Total number of new orders this month',
            'orders_by_size': 'Shirt orders by size',
        }
        
        this.action = useService("action")
        this.statistics= useState(useService("statisticsService"))

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

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
