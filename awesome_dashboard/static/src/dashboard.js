/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboardItem";
import { PieChart } from "./pie/pie";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  setup() {
    this.statisticsService = useService("awesome_dashboard.statistics");
    this.state = useState({
      res: this.statisticsService.data,
      avg_quantity: Number,
      avg_time: Number,
      nb_cancel: Number,
      nb_new: Number,
      tot_amount: Number,
      order_by_size: {
        type: Object,
      },
    });

    onWillStart(async () => {
      try {
        this.state.avg_quantity = this.state.res.average_quantity;
        this.state.avg_time = this.state.res.average_time;
        this.state.nb_cancel = this.state.res.nb_cancelled_orders;
        this.state.nb_new = this.state.res.nb_new_orders;
        this.state.tot_amount = this.state.res.total_amount;
        this.state.order_by_size = this.state.res.orders_by_size;
      } catch (error) {
        console.error("RPC Error:", error);
      }
    });
    this.action = useService("action");
    this.display = {
      controlPanel: {},
    };
  }
  static components = {
    Layout,
    DashboardItem,
    PieChart,
  };
  openCustomersView() {
    this.action.doAction("base.action_partner_form");
  }

  async openLeadsView() {
    this.action.doAction({
      name: "Leads",
      type: "ir.actions.act_window",
      res_model: "crm.lead",
      view_mode: "list,form",
      views: [
        [false, "list"],
        [false, "form"],
      ],
      target: "current", // Opens in the same window
    });
  }
}
registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
