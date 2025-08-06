/** @odoo-module **/

import { Component, onMounted, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statisticsService");
        this.state = useState({
            response: this.statisticsService.response
        });

        this.intervalId = null;
        this.items = registry.category("awesome_dashboard").get("awesome_dashboard.dashboard");

        onMounted(() => {
            this.intervalId = this.statisticsService.startInterval();
        })

        onWillUnmount(() => {
            if (!this.intervalId) return;
            clearInterval(this.intervalId);
        })
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: "current",
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
