import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class DashboardSettings extends Component {
  static template = "awesome_dashboard.DashboardSettings"
  static components = { Dialog, CheckBox }
  static props = {
    close: Function,
    all: {
      type: Array,
      element: { type: Object, shape: { id: String, description: String, "*": true } }
    },
    disabled: {
      type: Array,
      element: { type: String },
    },
    onToggle: Function
  }

  setup() {
    this.items = useState(this.props.all.map(item => ({ ...item, enabled: !this.props.disabled.includes(item.id) })))
  }

  handleToggle(checked, item) {
    item.enabled = checked
    this.props.onToggle(checked, item.id)
  }

  handleClose() {
    this.props.close()
  }
}
