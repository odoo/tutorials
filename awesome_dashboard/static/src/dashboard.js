/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, onWillStart } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.openCustomerKanban = this.openCustomerKanban.bind(this);
        this.openLeads = this.openLeads.bind(this);
        this.action = useService("action");
        onWillStart(async () => {
            this.stats = await rpc("/awesome_dashboard/statistics");
        });
    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            target: "current",
            res_id: "awesome_dashboard.action_lead_view_form",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        })
    }

    static components = { Layout, DashboardItem };
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
