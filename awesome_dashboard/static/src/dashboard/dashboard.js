/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./dashboard_item/pie_chart/pie_chart";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  setup() {
    this.display = {
      controlPanel: {},
    };
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
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
  .category("lazy_components")
  .add("awesome_dashboard.lazy_dashboard", AwesomeDashboard);
