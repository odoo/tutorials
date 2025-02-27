/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pieChart/pie_chart";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };
  setup() {
    this.action = useService("action");

    /*
    // removed in new owl update - odoo version 17.4

    this.rpc = useService(rpc);
    onWillStart(async () => {
      this.statistics = await this.rpc("/awesome_dashboard/statistics");
    });
    */

    this.statistics = useState(useService("awesome_dashboard.statistics"));
    // onWillStart(async () => {
    //   // this.statistics = await rpc("/awesome_dashboard/statistics");
    //   try {
    //     this.statistics = await this.statistics.loadStatistics();
    //     console.log(this.statistics);
    //   } catch (error) {
    //     console.error("statistics.loadStatistics  method failed:", error);
    //   }
    // });

    this.items = items;
  }

  openCustomersKanbanView() {
    this.action.doAction("base.action_partner_form");
  }
  async openLeadView() {
    this.action.doAction({
      type: "ir.actions.act_window",
      target: "new",
      res_model: "crm.lead",
      views: [
        [false, "form"],
        [false, "list"],
      ],
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
