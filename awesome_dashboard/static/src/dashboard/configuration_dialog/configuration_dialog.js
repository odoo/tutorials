import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useChildRef } from "@web/core/utils/hooks";

export class ConfigurationDialog extends Component {
  static template = "awesome_dashboard.ConfigurationDialog";
  static components = { Dialog };
  static props = { items: Array, close: Function };

  setup() {
    super.setup();
    this.modalRef = useChildRef();
    this.state = useState({
      config: JSON.parse(localStorage.getItem("dashboard_config")),
    });
  }

  onCloseClicked() {
    localStorage.setItem("dashboard_config", JSON.stringify(this.state.config));
    this.props.close?.();
  }
}
