import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };
  setup() {
    this.items = items;
    this.action = useService("action");
    this.statistics = useService("awesome_dashboard.statistics");
    this.state = useState(this.statistics.state);
  }
  openCustomer() {
    this.action.doAction("base.action_partner_form");
  }
  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
