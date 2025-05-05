/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {
        Layout,
        DashboardItem
    };

    async setup() {
        this.action = useService("action");
        console.log("test");
        this.statisticsService = useService("statistics");

        onWillStart(async () => {
            this.statistics = await this.statisticsService.getStatisticsMemoize();
        });
        console.log(this.statistics);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
