import { Component, useState, reactive } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { DashboardItem } from "./dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { user } from "@web/core/user";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";

  setup() {
    this.action = useService("action");
    this.state = useState({ statistics: useService("statistics"), config: {} });
    this.items = registry.category("awesome_dashboard").getAll();

    if (!user.settings.dashboard_config) {
      this.state.config = this.initializeDashboardConfig();
    } else {
      this.state.config = JSON.parse(user.settings.dashboard_config);
    }
    this.dialogService = useService("dialog");
  }

  initializeDashboardConfig() {
    const dashboard_config = this.items.reduce((acc, item) => {
      acc[item.id] = true;
      return acc;
    }, {});

    user.setUserSettings("dashboard_config", JSON.stringify(dashboard_config));
    return dashboard_config;
  }

  updateUserSettings() {
    this.state.config = JSON.parse(user.settings.dashboard_config);
  }
  sDSA;

  showCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  showLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: _t("Leads"),
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  showConfigurationDialog(ev) {
    console.log(user.settings);
    ev?.stopPropagation();
    this.dialogService.add(
      ConfigurationDialog,
      {
        items: this.items,
      },
      {
        context: this,
        onClose: this.updateUserSettings.bind(this),
      }
    );
  }

  static components = { Layout, DashboardItem, ConfigurationDialog };
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
