import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog"
import { registry } from "@web/core/registry";


export class SettingsDialog extends Component {
  static template = "awesome_dashboard.settings_dialog";
  static props = ['close'];
  static components = { Dialog };

  setup() {
    this.state = useState({ items: {} });

    const items = registry.category("awesome_dashboard").getAll();

    const filtered_ids = localStorage.getItem("awesome_dashboard.displayed_items") ?? [];

    for (var i of items) {
      this.state.items[i.id] = { display: !filtered_ids.includes(i.id), description: i.description };
    }
    this.toggleDisplay = this.toggleDisplay.bind(this);
    this.onSave = this.onSave.bind(this);
  }

  toggleDisplay(id) {
    this.state.items[id].display = !this.state.items[id].display;
  }

  onSave() {
    const filtered_ids = Object.entries(this.state.items)
      .filter(([id, item]) => !item.display)
      .map(([id]) => id);

    localStorage.setItem("awesome_dashboard.displayed_items", filtered_ids)
    this.props.close();
  }

}
