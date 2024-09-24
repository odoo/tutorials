/** @odoo-module **/

import {Component, onWillStart} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "./dashboard_item/dashboard_item";
import {PieChart} from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart};

    setup() {
        this.action = useService("action");
        this.statistics = useService("statistics_service");
        this.display = {
            controlPanel: {}
        }
        onWillStart(async () => {
            this.stats = await this.statistics.loadStatistics();
        })
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: "current",
        })
    }
}


registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
