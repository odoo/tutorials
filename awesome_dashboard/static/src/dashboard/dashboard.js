/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { DashboardDialog } from "./dashboard_dialog/dashboard_dialog";
import { reactive } from "@odoo/owl";
import { user } from "@web/core/user";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, DashboardDialog };

  async setup() {
    this.orm = useService("orm");
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.items = registry.category("awesome_dashboard").getAll();
    this.dialog = useService("dialog");

    this.display = {
      controlPanel: {},
    };

    onMounted(async () => {
      let result = await this.loadDashboard();

      if (result.length === 0) {
        this.items.forEach((item) => {
          this.displayedItems.add(item.id);
        });
      } else {
        result.forEach((item) => {
          this.displayedItems.add(item);
        });
      }
    });

    this.displayedItems = useState(reactive(new Set()));
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  openConfiguration() {
    this.dialog.add(DashboardDialog, {
      onConfirm: (displayedItems) => {
        this.displayedItems.clear();
        displayedItems.forEach((id) => this.displayedItems.add(id));
        this.saveDashboard(displayedItems);
      },
    });
  }

  async saveDashboard(data) {
    await this.orm.write("res.users", [user.userId], {
      dashboard_config: JSON.stringify(data),
    });
  }

  async loadDashboard() {
    const result = await this.orm.read(
      "res.users",
      [user.userId],
      ["dashboard_config"]
    );
    return JSON.parse(result[0]["dashboard_config"] || "[]");
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
