/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem } ;

    setup(){
        this.actions = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.display = { controlPanel: {} };

        onWillStart(async () => {
            this.statistics = await this.statisticsService.loadStatistics();
        })
    }

    openCustomersView(){
        this.actions.doAction("base.action_partner_form");
    }

    openAllLeads(){
        this.actions.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);