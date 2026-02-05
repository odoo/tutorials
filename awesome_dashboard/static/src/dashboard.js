import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardItem } from "./dashboarditem/dashboarditem"

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  setup() {
    this.action = useService("action");
    this.statisticsService = useService("awesome_dashboard.statistics");
    this.display = {
      controlPanel: {},
    };
    this.state = useState({
      loading: true,
    });

    onWillStart(async () => {
      this.statistics = await this.statisticsService.loadStatistics();
      console.log(this.statistics);
    });

    onMounted(async () => {
      await new Promise((res) => setTimeout(res, 1500));
      this.state.loading = false;
    });
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
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
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
