/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { Piechart } from "./pieChart/pieChart";
class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, Piechart };

  setup() {
    this.action = useService("action");
    const dashboardItemsRegistryData = registry.category("awesome_dashboard");
    this.items = dashboardItemsRegistryData.getAll();
    this.statisticServices = useService("awesome_dashboard.statistics");
    this.state = useState({ statistic: this.statisticServices.statistic });
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

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
