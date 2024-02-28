/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  async setup() {
    this.action = useService("action");
    this.rpc = useService("rpc");
    this.statistics = useState(useService("statistics"));
    this.dialog = useService("dialog");
    this.items = registry
      .category("dashboard_items")
      .contains("awesome_dashboard")
      ? registry.category("dashboard_items").get("awesome_dashboard")
      : [];
    this.state = useState({
      uncheckedItems:
        browser.localStorage.getItem("uncheckedItems")?.split(",") || [],
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

  openConfiguration() {
    this.dialog.add(ConfigurationDialog, {
      items: this.items,
      uncheckedItems: this.state.uncheckedItems,
      updateConfiguration: this.updateConfiguration.bind(this),
    });
  }

  updateConfiguration(uncheckedItems) {
    this.state.uncheckedItems = uncheckedItems;
  }
}

class ConfigurationDialog extends Component {
  static template = "awesome_dashboard.ConfigurationDialog";
  static components = { Dialog, CheckBox };

  setup() {
    this.items = useState(
      this.props.items.map((item) => ({
        ...item,
        checked: !this.props.uncheckedItems.includes(item.id),
      }))
    );
  }

  done() {
    this.props.close();
  }

  onChange(checked, item) {
    item.checked = checked;
    const newUncheckedItems = Object.values(this.items)
      .filter((item) => !item.checked)
      .map((item) => item.id);

    browser.localStorage.setItem("uncheckedItems", newUncheckedItems);
    this.props.updateConfiguration(newUncheckedItems);
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
