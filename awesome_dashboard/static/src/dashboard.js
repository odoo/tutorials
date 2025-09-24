/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { DashboardItem } from "./dashboard_item";
import { Component, useState, onWillStart } from "@odoo/owl";
    
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics")
        onWillStart(async () => {
            this.result = await this.statistics.data();
        })
    }   

    openCustomers() {
        this.action.doAction('base.action_partner_form'); // get the action by its XML ID
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
