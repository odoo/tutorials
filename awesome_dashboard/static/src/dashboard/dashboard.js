import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { DashboardItem } from "./dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";

  setup() {
    this.action = useService("action");
    this.statistics = useState(useService("statistics"));
    this.items = registry.category("awesome_dashboard").getAll();
    this.config = useState(
      JSON.parse(localStorage.getItem("dashboard_config"))
    );
    this.dialogService = useService("dialog");
  }

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
    ev?.stopPropagation();
    this.dialogService.add(
      ConfigurationDialog,
      {
        items: this.items,
      },
      {
        context: this,
        onClose: () => {
          this.config = JSON.parse(localStorage.getItem("dashboard_config"));
        },
      }
    );
  }

  static components = { Layout, DashboardItem, ConfigurationDialog };
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
