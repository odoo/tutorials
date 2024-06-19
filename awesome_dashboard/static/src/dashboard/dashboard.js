/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };
  static props = [];

  setup() {
    this.actionService = useService("action");
    this.dialogService = useService("dialog");
    this.stats = useState(useService("awesome_dashboard.statistics"));
    this.items = registry.category("awesome_dashboard").getAll();
    this.state = useState({
      disabledItems:
        browser.localStorage
          .getItem("awesome_dashboard.disabled_dashboard_items")
          ?.split(",") || [],
    });
  }

  openCustomerView() {
    this.actionService.doAction("base.action_partner_form");
  }

  openLeads() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "All leads",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  openConfiguration() {
    this.dialogService.add(ConfigurationDialog, {
      items: this.items,
      disabledItems: this.state.disabledItems,
      onUpdateConfiguration: this.updateConfiguration.bind(this),
    });
  }

  updateConfiguration(newDisabledItems) {
    this.state.disabledItems = newDisabledItems;
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
