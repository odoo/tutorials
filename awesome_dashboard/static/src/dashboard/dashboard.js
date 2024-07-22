/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboardItem";
import { items } from "./items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = items;
    }

    openCustomerView() {
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

    async updateStatistics() {
        this.statistics = await this.rpc("/awesome_dashboard/statistics");
        setInterval(async () => {
            this.statistics = await this.rpc("/awesome_dashboard/statistics");
        }, 10000);
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
