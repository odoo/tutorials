import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { DashboardSettingsDialog } from "./dashboard_settings/dashboard_settings_dialog";
import "./dashboard_items";
import "./statistics_service";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.NiceAndAwesomeDashboard";
  static components = { Layout, DashboardItem, DashboardSettingsDialog };
  setup() {
    this.action = useService("action");
    this.dialog = useService("dialog");
    this.statistics = useService("awesome_dashboard.statistics");
    this.state = useState(this.statistics);
    this.allItems = registry.category("awesome_dashboard").getAll();
    this.settings = useState({
      removedIds: [],
      items: this.allItems,
    });
  }
  openSettingsDialog() {
    this.dialog.add(DashboardSettingsDialog, {
      items: this.allItems,
      removedIds: this.settings.removedIds,
      onApply: (removedIds) => this.applySettings(removedIds),
    });
  }
  applySettings(removedIds) {
    this.settings.removedIds = removedIds;
    this.settings.items = this.allItems.filter(
      (item) => !removedIds.includes(item.id)
    );
  }
  openSettings() {
    this.action.doAction("base.action_partner_form");
  }
  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Crm Leads",
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "form"],
        [false, "list"],
      ],
    });
  }
}

registry
  .category("lazy_components")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
