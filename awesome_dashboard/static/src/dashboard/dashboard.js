/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { Piechart } from "./piechart";
import { registry } from "@web/core/registry";
import { DBModal } from "./dashboard_setting_modal";

export class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";

  static components = { Layout, DashboardItem, Piechart };

  setup() {
    this.action = useService("action");
    this.statisticService = useService("load_statistics");
    this.data = useState(this.statisticService);
    this.dialog = useService("dialog");
  }

  openMyModal() {
    this.dialog.add(DBModal, {
      items: this.data.stats,
      chart: this.data.chartData,
    });
  }

  viewCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  viewLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "form"],
        [false, "list"],
      ],
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
