/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = {
            controlPanel : {},
        }
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
  }
  openCustomer() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
        type: "ir.actions.act_window",
        name: "Leads",
        res_model: "crm.lead",
        views: [[false, "list"], [false, "form"]],
        target: "current",
    });
  }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
