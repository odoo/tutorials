import { Component, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { isVisible } from "@web/core/utils/ui";

export class SettingsDialog extends Component {
  static template = "awesome_dashboard.SettingsDialog";
  static components = { Dialog, CheckBox };
  static props = {
    items: Array,
    invisibleItems: Array,
    onSubmit: Function,
    close: Function,
  };

  setup() {
    this.items = useState(
      this.props.items.map((item) => ({
        ...item,
        isVisible: !this.props.invisibleItems.includes(item.id),
      })),
    );
  }

  onCheckboxChanged(itemToChange, isChecked) {
    itemToChange.isVisible = isChecked;
  }

  onApply() {
    this.props.close();
    this.props.onChange(
      this.items
        .filter((item) => !item.isVisible)
        .map((item) => {
          return item.id;
        }),
    );
  }
}
