/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { Piechart } from "./piechart";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";

  setup() {
    this.action = useService("action");
    this.statistics = useService("awesome_dashboard.statistics")
    onWillStart(async () => {
        this.result = await this.statistics.loadStatistics()
    })
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
        type:'ir.actions.act_window',
        name:'Leads',
        target:'current',
        res_model:'crm.lead',
        views:[[false,'list'],[false,'form']]
    });
  }

  static components = { Layout, DashboardItem, Piechart };
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
