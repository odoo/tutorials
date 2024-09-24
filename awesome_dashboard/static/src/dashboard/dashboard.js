/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
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
        this.stats = useState(useService("statistics_service"));
        this.display = {
            controlPanel: {}
        };
        this.items = registry.category("awesome_dashboard").getAll();
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


registry.category("lazy_components").add("awesome_dashboard", AwesomeDashboard);
