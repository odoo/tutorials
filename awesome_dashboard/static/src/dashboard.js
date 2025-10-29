/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {
        Layout,
        DashboardItem
    };

    static props = {
        display : {
            controlPanel: {}
        },
    }

    setup() {
        this.action = useService("action");
        const statsService = useService("awesome_dashboard.getStats");

        onWillStart(async () => {
            this.result = await statsService.loadStatistics();
        });
    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    async openActivity() {
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
