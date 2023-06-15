/** @odoo-module **/

import {Component,useSubEnv,onWillStart,useEffect,useRef} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { Card } from "./card/card";
import { loadJS } from "@web/core/assets";

class AwesomeDashboard extends Component {
  setup() {
    useSubEnv({
      config: {
        ...getDefaultConfig(),
        ...this.env.config,
      },
    });
    this.display = {
      controlPanel: { "top-right": false, "bottom-right": true },
    };
    this.action = useService("action");
    // this.rpc = useService("rpc");
    this.myService = useService("myService");

    this.keys = {
      nb_new_orders: this.env._t("Number of new orders this month"),
      total_amount: this.env._t("Total amount of new orders this month"),
      average_quantity: this.env._t(
        "Average amount of t-shirt by order this month"
      ),
      nb_cancelled_orders: this.env._t("Number of cancelled orders this month"),
      average_time: this.env._t(
        "Average time for an order to go from 'new' to 'sent' or 'cancelled'"
      ),
    };

    this.canvasRef = useRef("canvas");
    this.chart = null;

    onWillStart(async () => {
      this.statistics = await this.myService.loadStatistics();
      await loadJS("/web/static/lib/Chart/Chart.js");
      // this.statistics = await this.rpc("/awesome_tshirt/statistics");
    });
    useEffect(() => this.renderChart());

    const effectService = useService("effect");
    effectService.add({
      type: "rainbow_man", 
      message: "Js Training Finished.",
    });
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    const config = this.canvasRef.el;
    this.chart = new Chart(config, {
      type: "pie",
      data: {
        labels: Object.keys(this.statistics["orders_by_size"]),
        datasets: [
          {
            data: Object.values(this.statistics["orders_by_size"]),
            backgroundColor: [
              "#DE3163",
              "#40E0D0",
              "#6495ED",
              "#A6ACAF",
              "#FFD700",
            ],
          },
        ],
      },
    });
  }

  customerview() {
    this.action.doAction("base.action_partner_form");
  }
  openSettings() {
    this.action.doAction("base_setup.action_general_configuration");
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
 Order() {
    const domain =
      "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]";
    this.openOrders("Last 7 days orders", domain);
  }
  
  Cancelled() {
    const domain =
      "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')), ('state','=', 'cancelled')]";
    this.openOrders("Last 7 days cancelled orders", domain);
  }
}

AwesomeDashboard.components = { Layout, Card };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
// registry.category("services").add("myService", myService);
