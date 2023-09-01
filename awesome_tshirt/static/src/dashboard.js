/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { getDefaultConfig } from "@web/views/view";
import { useSetupAction } from "@web/webclient/actions/action_hook";
import { useEnrichWithActionLinks } from "@web/webclient/actions/reports/report_hook";
import { Domain } from "@web/core/domain";
import { Card } from "./Card/card";
import { tshirtStatsService } from "./tshirtStats_service";


import { Component, useSubEnv, onWillStart } from "@odoo/owl";

class AwesomeDashboard extends Component {
  setup() {
    this.display = {
      controlPanel: { "top-right": false, "bottom-right": false },
    };
    this.action = useService("action");
    this.rpc = useService("rpc");
    this.tshirtStatService = useService("tshirtStatService");

    useSubEnv({
      config: {
        ...getDefaultConfig(),
        ...this.env.config,
      },
    });
    this.keyToString = {
      average_quantity: "Average amount of t-shirt by order this month",
      average_time:
        "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
      nb_cancelled_orders: "Number of cancelled orders this month",
      nb_new_orders: "Number of new orders this month",
      total_amount: "Total amount of new orders this month",
    };

    async function fetchStats() {
      this.statistics = await this.tshirtStatService.loadStatistics();
    }
    onWillStart(fetchStats);
  }

  viewCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openOrders(title, domain) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: title,
      res_model: "awesome_tshirt.order",
      domain: new Domain(domain).toList(),
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
  openRecentOrders() {
    const domain =
      "[('create_date','>=',(context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]";
    this.openOrders("Last 7 days Orders", domain);
  }
  openCancelledOrders() {
    const domain = "[('state','=','cancelled')]";
    this.openOrders("Cancelled Orders", domain);
  }
}

AwesomeDashboard.components = { Layout,Card };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
