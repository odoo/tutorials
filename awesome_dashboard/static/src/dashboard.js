import { Component, onWillStart } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboardItem/dashboardItem";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        const statisticsService = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            this.statistics = await statisticsService.loadStatistics();
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t("CRM Leads"),
            res_model: 'crm.lead',
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
