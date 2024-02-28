/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./Dashboard_item/Dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.rpc = useService("rpc");

        this.state = useState({ statistics: {} });

        onWillStart(async () => {
            const result = await this.rpc("/awesome_dashboard/statistics", { a: 1, b: 2 });
            this.updateStatistics(result);
        });


    }

    updateStatistics(new_statistics) {
        this.state.statistics = new_statistics
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
