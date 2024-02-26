/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  async setup() {
    this.action = useService("action");
    this.rpc = useService("rpc");
    this.statistics = useService("statistics");
    onWillStart(async () => {
      this.updateStatistics(await this.statistics());
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
        [false, "tree"],
        [false, "form"],
      ],
    });
  }

  updateStatistics(data) {
    this.newOrders = data.nb_new_orders;
    this.totalOrders = data.total_amount;
    this.averageTshirt = data.average_quantity;
    this.cancelledOrders = data.nb_cancelled_orders;
    this.averageTime = data.average_time;
  }
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
