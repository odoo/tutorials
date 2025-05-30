/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item.js";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = {
            controlPanel: {}
        };
        this.action = useService("action");
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
