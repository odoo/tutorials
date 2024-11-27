import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useChildRef } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

export class ConfigurationDialog extends Component {
  static template = "awesome_dashboard.ConfigurationDialog";
  static components = { Dialog };
  static props = { items: Array };

  setup() {
    super.setup();
    this.modalRef = useChildRef();
    this.state = useState({
      config: JSON.parse(user.settings.dashboard_config || "null"),
    });
  }

  async onCloseClicked() {
    await user.setUserSettings(
      "dashboard_config",
      JSON.stringify(this.state.config)
    );
    this.props.close?.();
  }
}
