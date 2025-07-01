/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout };
    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState({ statistics: null });

        onWillStart(async () => {
            this.state.statistics = await this.statisticsService.loadStatistics();
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form"); // Predefined action for res.partner (customers)
    }

    openLeadsView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
