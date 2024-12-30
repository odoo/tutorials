/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { SettingsDialog } from "./settings_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  setup() {
    this.action = useService("action");
    this.dialogService = useService("dialog");
    this.stats = useState(useService("statistics"));
    this.items = registry.category("awesome_dashboard").get("dashboard_items");
    this.invisibleItems = useState(
      browser.localStorage.getItem("invisibleItems")?.split(",") ?? [],
    );
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  async openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Leads",
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  openDialog() {
    this.dialogService.add(SettingsDialog, {
      items: this.items,
      invisibleItems: this.invisibleItems,
      onChange: this.onVisibleItemsChanged,
    });
  }

  onVisibleItemsChanged(updatedItems) {
    browser.localStorage.setItem("invisibleItems", updatedItems.join(","));
    this.invisibleItems = updatedItems;
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
