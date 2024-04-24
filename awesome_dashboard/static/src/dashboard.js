/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"
import { onWillStart } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item/dashboard_item"
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup(){
        this.statisticsDescription = {
            'average_quantity':'Average amount of t-shirt by order this month',
            'average_time':'Average time for an order to get from "new" to "sold" or "canceled"',
            'nb_cancelled_orders':'Number of canceled orders this month',
            'nb_new_orders':'Number of new orders this month',
            'total_amount':'Total number of new orders this month',
        }
        
        this.action = useService("action")
        this.statisticsService = useService("statisticsService")

        onWillStart(async () => {
            this.statistics = await this.statisticsService.loadStatistics()
        })
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
