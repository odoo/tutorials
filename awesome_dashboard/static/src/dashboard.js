/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./component/dashboardItem/dashboardItem";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup = () => {
        this.action = useService("action");
        onWillStart(async () => {
            this.res = await rpc("/awesome_dashboard/statistics");
        });
    }

    showCustomers = () => {
        this.action.doAction("base.action_partner_form");
    }

    showLeads = () => {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
