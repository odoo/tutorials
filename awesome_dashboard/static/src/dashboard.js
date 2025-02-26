/** @odoo-module **/

import { Component, useState, onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/dashboardItem";
import { PieChart } from "./PieChart/pieChart";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart}

    setup() {
        this.action = useService("action");
        this.dashboardData = useService("awesome_dashboard.statistics");
        
        console.log(this.dashboardData);
        
        onWillStart(async () => {
            this.dashboardData = await this.dashboardData.loadStatistics();
        });
    }

    viewCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    openActivity(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: ('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
