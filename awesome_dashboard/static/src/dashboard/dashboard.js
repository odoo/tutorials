import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard-item/dashboard-item";
import { SettingsDialog } from "./settings-dialog/settings-dialog";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };
  static props = [];

  setup() {
    this.action = useService("action");
    const statisticsService = useService("awesome_dashboard.statistics");
    this.dialog = useService('dialog');

    this.statistics = useState(statisticsService);

    this.state = useState({ items: this.getDisplayedItems() });

  }

  getDisplayedItems() {
    const filtered_item_ids = localStorage.getItem("awesome_dashboard.displayed_items") ?? [];
    return registry
      .category("awesome_dashboard")
      .getAll()
      .filter((item) => !filtered_item_ids.includes(item.id));
  }

  reloadDashboard() {
    this.state.items = this.getDisplayedItems();
  }

  openPartnerForm() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: 'ir.actions.act_window',
      name: 'Leads',
      res_model: 'crm.lead',
      views: [[false, 'list'], [false, 'form']],
    });
  }

  openSettingsDialog() {
    this.dialog.add(SettingsDialog, {}, { onClose: () => this.reloadDashboard() });
  }

}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
