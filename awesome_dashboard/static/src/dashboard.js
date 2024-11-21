/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem };

    async setup() {
        this.action = useService("action");
        this.stat = useService("awesome_dashboard.statistics");
        this.data = useState({});

        onWillStart(async () => {
            this.data = await this.stat();
            this.data = await this.stat();

        });
    }
    openCustomerView() {
        this.action.doAction(
            "base.action_partner_form"
        );
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: 'current',
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
