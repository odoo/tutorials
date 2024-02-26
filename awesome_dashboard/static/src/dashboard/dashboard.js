/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigurationDialog } from "./dahsboard_dialog/dashboard_dialogue";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, ConfigurationDialog };

  setup() {
    this.display = {
      controlPanel: {},
    };
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.items = registry.category("awesome_dashboard_items").getAll();
    this.dialog = useService("dialog");
    this.state = useState({
      disabledItems: [],
    });

    const user = useService("user");

    onWillStart(async () =>
      this.updateConfiguration(user.settings["stats_visibility"])
    );
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
}

registry
  .category("lazy_components")
  .add("awesome_dashboard.lazy_dashboard", AwesomeDashboard);
