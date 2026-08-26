import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { Layout } from "@web/search/layout"

import { DashboardItem } from "./components/dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        const dashboardService = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            this.statistics = await dashboardService.loadStatistics()
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads(activity) {
        /* Dynamic action to open Leads with only list and form view */

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
