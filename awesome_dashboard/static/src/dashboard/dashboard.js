import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./piechart/PieChart";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  setup() {
    this.action = useService("action");
    this.display = {
      controlPanel: {},
    };
    this.statistics = useState(useService("awesome_dashboard.statistics"));
  }

  openCustomer() {
    this.action.doAction("base.action_partner_form");
  }

  openLead() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Leads",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
