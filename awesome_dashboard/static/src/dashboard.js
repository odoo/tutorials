/** @odoo-module **/

import { Component, useState, onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.state = useState({ statistics: null });

        onWillStart(async () => {
        this.state.statistics = await rpc("/awesome_dashboard/statistics");
        });
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }
    async openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);

export { AwesomeDashboard };
