import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { DashboardSettings } from "./dashboard_settings";
import { browser } from "@web/core/browser/browser";

const storageKey = "dashboardDisabled"

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  setup() {
    this.action = useService("action");
    this.dialog = useService("dialog");
    this.stats = useState(useService("awesome_dashboard.statistics"));

    this.items = registry.category("awesome_dashboard").getAll()
    this.disabled = useState(browser.localStorage.getItem(storageKey)?.split(",") || [])
  }

  handleCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  handleLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Leads",
      res_model: "crm.lead",
      views: [[false, "list"], [false, "form"]],
    });
  }

  openSettings() {
    this.dialog.add(DashboardSettings, {
      all: this.items,
      disabled: this.disabled,
      onToggle: this.handleToggle,
    })
  }

  closeSettings() {
    this.settings = false
  }

  handleToggle(checked, id) {
    if (checked) {
      const index = this.disabled.indexOf(id);
      if (index !== -1) {
        this.disabled.splice(index, 1);
      }
    } else {
      if (!this.disabled.includes(id)) {
        this.disabled.push(id);
      }
    }

    browser.localStorage.setItem(storageKey, this.disabled.join(","))
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
