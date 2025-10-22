import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";

export class DashboardDialog extends Component {
  static template = "awesome_dashboard.DashboardDialog";
  static components = { Dialog };
  static props = ["close", "onConfirm"];

  setup() {
    this.title = _t("Dashboard Configuration");
    this.items = registry.category("awesome_dashboard").getAll();
    this.state = useState({
      displayedItems: new Set(
        browser.localStorage.getItem("selectedDashboardItems")?.split(",") || []
      ),
    });
    if (this.state.displayedItems.size === 0) {
      this.items.forEach((item) => {
        this.state.displayedItems.add(item.id);
      });
    }
  }

  toggleItem(item) {
    if (this.state.displayedItems.has(item)) {
      this.state.displayedItems.delete(item);
    } else {
      this.state.displayedItems.add(item);
    }
  }

  confirm() {
    this.props.onConfirm([...this.state.displayedItems]);
    this.props.close();
  }
}
