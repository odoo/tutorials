import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { PieChart } from "./pieChart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };
  setup() {
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.items = registry.category("awesome_dashboard").getAll();
    this.dialog = useService("dialog");
    this.state = useState({
      disabledItems:
        browser.localStorage.getItem("disabledDashboardItems")?.split(",") ||
        [],
    });
  }

  openConfiguration() {
    this.dialog.add(ConfigurationDialog, {
      items: this.items,
      disabledItems: this.state.disabledItems,
      onUpdateConfiguration: this.updateConfiguration.bind(this),
    });
  }

  updateConfiguration(newDisabledItems) {
    this.state.disabledItems = newDisabledItems;
  }

  openCustomersKanbanView() {
    this.action.doAction("base.action_partner_form");
  }

  async openLeadView() {
    this.action.doAction({
      type: "ir.actions.act_window",
      target: "new",
      res_model: "crm.lead",
      views: [
        [false, "form"],
        [false, "list"],
      ],
    });
  }
}
class ConfigurationDialog extends Component {
  static template = "awesome_dashboard.ConfigurationDialog";
  static components = { Dialog, CheckBox };
  static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

  setup() {
    this.items = useState(
      this.props.items.map((item) => {
        return {
          ...item,
          enabled: !this.props.disabledItems.includes(item.id),
        };
      })
    );
    this.newDisabledItems;
  }

  done() {
    browser.localStorage.setItem(
      "disabledDashboardItems",
      this.newDisabledItems
    );
    this.props.onUpdateConfiguration(this.newDisabledItems);
    this.props.close();
  }

  onChange(checked, changedItem) {
    changedItem.enabled = checked;
    this.newDisabledItems = Object.values(this.items)
      .filter((item) => !item.enabled)
      .map((item) => item.id);
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
