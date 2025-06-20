/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { rpc } from "@web/core/network/rpc";
class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  setup() {
    this.action = useService("action");
    this.state = useState({ statistic: null });

    onWillStart(async () => {
      this.state.statistic = await rpc("/awesome_dashboard/statistics");
    });
  }
  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  async openLeads(activity) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Journal Entry",
      target: "current",
      res_id: activity.res_id,
      res_model: "crm.lead",
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
