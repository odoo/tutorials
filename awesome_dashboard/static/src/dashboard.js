/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };
  setup() {
    this.action = useService("action");
  }

  openCustomersKanbanView() {
    this.action.doAction("base.action_partner_form");
  }
  async openLeadView() {
    this.action.doAction({
      type: "ir.actions.act_window",
      target: "new",
      res_model: "crm.lead",
      views: [
        [false, "form"],
        [false, "list"],
      ],
    });
  }
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
