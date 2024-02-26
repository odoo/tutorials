/** @odoo-module **/

import {Component, onWillStart} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {DashboardItem} from "./dashboarditem/dashboarditem"
import {useService} from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem}

    setup() {
        this.display = {
            controlPanel: {}
        };
        this.action = useService("action");
        this.dashboardService = useService("dashboard");
        onWillStart(async () => {
            this.result = await this.dashboardService.loadStatistics();
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
