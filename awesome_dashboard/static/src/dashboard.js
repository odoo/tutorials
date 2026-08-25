import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard-item/dashboard-item";
import { DashboardNumberItem } from "./dashboard-number-item/dashboard-number-item";
import { PieChart } from "./pie-chart/pie-chart";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, DashboardNumberItem, PieChart };

  setup() {
    this.action = useService("action");
    const statisticsService = useService("awesome_dashboard.statistics");

    this.result = useState(statisticsService);
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
