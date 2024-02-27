/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  async setup() {
    this.action = useService("action");
    this.rpc = useService("rpc");
    this.statistics = useState(useService("statistics"));
    console.log(this.statistics);
    // onWillStart(async () => {
    //   this.updateStatistics(await this.statistics());
    //   this.updateTimer = setInterval(async () => {
    //     this.updateStatistics(await this.statistics());
    //   }, 5000);
    // });
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Leads",
      res_model: "crm.lead",
      views: [
        [false, "tree"],
        [false, "form"],
      ],
    });
  }

  //   updateStatistics(data) {
  //     this.state.newOrders = data.nb_new_orders;
  //     this.state.totalOrders = data.total_amount;
  //     this.state.averageTshirt = data.average_quantity;
  //     this.state.cancelledOrders = data.nb_cancelled_orders;
  //     this.state.averageTime = data.average_time;
  //     this.state.pieChartLabels = Object.keys(data.orders_by_size);
  //     this.state.pieChartData = Object.values(data.orders_by_size);
  //   }
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
