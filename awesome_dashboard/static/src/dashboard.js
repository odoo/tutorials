/** @odoo-module **/

import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

import { Component, onWillStart } from "@odoo/owl";

import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.stats = useService("awesome_dashboard.statistics");
        this.display = {
            ControlPanel: {},
        };

        onWillStart(async () => {
            this.stats = await this.stats.loadStatistics();
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
