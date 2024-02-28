/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item/dashboard_item"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , AwesomeDashboardItem };

    setup() {
        this.action = useService("action");
        this.display = {
            controlPanel: {},
        };
        this.rpc = useService("rpc");
        onWillStart(async () => {
            this.result_statistics = await this.rpc("/awesome_dashboard/statistics");
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type:"ir.actions.act_window",
            name:"Leads",
            res_model:"crm.lead",
            views:[
                [false,"list"],
                [false,"form"]
            ]
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
