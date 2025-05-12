/** @odoo-module **/

import { Component, onWillStart  } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService} from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart} from "./pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, AwesomeDashboardItem, PieChart }

    static props = {
        action: Object,
        actionId: Number,
        updateActionState: Function,
        className: String,
    };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.Statistics");
        onWillStart(async () => {
            this.result = await rpc("/awesome_dashboard/statistics");
            this.statistics = await this.statistics
        })
    }
    openSettings() {
          this.action.doAction("base_setup.action_general_configuration");
    }

    openActivityCustomers(activity) {
        console.log("clicked button Customers")
        this.action.doAction("base.action_partner_form");
    }

    async openActivityLeads(activity) {
        console.log("clicked button Leads")
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            res_model: 'crm.lead',
            views: [[false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
