/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  setup() {
    this.display = {
      controlPanel: {},
    };
    this.action = useService("action");
    this.statisticsService = useService("awesome_dashboard.statistics");

    onWillStart(async () => {
     this.statistics = await this.statisticsService.load()
    });
  }
  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      res_model: "crm.lead",
      name: "Leads",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
