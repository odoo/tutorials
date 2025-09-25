import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./pie_chart";
import { DashboardItem } from "./dashboard_item";

import { Component, onWillStart, useState } from "@odoo/owl";
    
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics")); // useState because it's reactive
    }   

    openCustomers() {
        this.action.doAction('base.action_partner_form');
    }

    openLeads(){
        this.action.doAction({ // define the action inline
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'form'],
                [false, 'list']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
