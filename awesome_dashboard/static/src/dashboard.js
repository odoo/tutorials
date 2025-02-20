import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./components/dashboard_item/dashboard_item";
import { PieChart } from "./components/Pie_chart/Pie_chart";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  setup() {
    this.action = useService("action");
    this.statistics = useService("awesome_dashboard.statistics");

    onWillStart(async () => {
      try {
        this.result = await this.statistics.loadStatistics();
      } catch (err) {
        console.log(`Error occured during the fetching of statistics : ${err}`);
      }
    });
  }

  showCustomers() {
    // doAction expects either an XML ID or an action dictionary
    this.action.doAction("base.action_partner_form");
  }

  showLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: _t("CRM Leads"),
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
