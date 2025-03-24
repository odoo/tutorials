/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService('action');
        
        this.statsService = useService('awesome_dashboard.stats');
        this.stats = this.statsService.test();


        onWillStart(async () => {
            this.stats = Object.entries(await this.statsService.getValuesMem()).filter((elt) => {return typeof(elt[1]) == typeof(1);});
            this.salesData = (await this.statsService.getValuesMem()).orders_by_size
        });

    }
    
    customersButton() {
        this.action.doAction('base.action_partner_form');
    }

    leadsButton() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
