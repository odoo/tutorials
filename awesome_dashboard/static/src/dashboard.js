/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component } from "@odoo/owl";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.openCustomerKanban = this.openCustomerKanban.bind(this);
        this.openLeads = this.openLeads.bind(this);
        this.action = useService("action");
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

    static components = { Layout };
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
