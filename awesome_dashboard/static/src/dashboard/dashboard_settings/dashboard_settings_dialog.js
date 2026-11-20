import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class DashboardSettingsDialog extends Component {
  static template = "awesome_dashboard.DashboardSettingsDialog";
  static components = { Dialog };
  static props = {
    close: Function,
    items: { type: Array },
    removedIds: { type: Array },
    onApply: Function,
  };

  setup() {
    this.state = useState(
      Object.fromEntries(
        this.props.items.map((item) => [
          item.id,
          !this.props.removedIds.includes(item.id),
        ])
      )
    );
  }

  onToggle(itemId, event) {
    this.state[itemId] = event.target.checked;
  }

  getDescription(item) {
    return _t(item.description);
  }

  apply() {
    const removedIds = this.props.items
      .filter((item) => !this.state[item.id])
      .map((item) => item.id);
    this.props.onApply(removedIds);
    this.props.close();
  }

  cancel() {
    this.props.close();
  }
}
