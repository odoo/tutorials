import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard-item/dashboard-item";
import { DashboardNumberItem } from "./dashboard-number-item/dashboard-number-item";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, DashboardNumberItem };

  setup() {
    this.action = useService("action");
    const statisticsService = useService("awesome_dashboard.statistics");
    onWillStart(async () => {
      this.result = await statisticsService.loadStatistics();
    });
  }

  openPartnerForm() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: 'ir.actions.act_window',
      name: 'Leads',
      res_model: 'crm.lead',
      views: [[false, 'list'], [false, 'form']],
    });
  }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
