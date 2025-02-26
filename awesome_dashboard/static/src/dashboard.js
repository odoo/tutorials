/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { PieChart } from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };
    setup(){
        this.action = useService("action")
        this.service = useService("awesome_dashboard.statistics")
        onWillStart(async()=>{
            this.result = await this.service.loadData();
        })
    }
    
    customersAction(){
        this.action.doAction("base.action_partner_form")
    }
    leadsAction(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [false, 'list'],
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
