/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import {rpc} from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    
    setup() {
        this.action = useService("action");
        this.orderStats = useState({});
        onWillStart(this.onWillStart);
    }
    
    async onWillStart() {

        this.orderStats.value = await rpc("/awesome_dashboard/statistics");
        console.log(this.orderStats.value);

    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
