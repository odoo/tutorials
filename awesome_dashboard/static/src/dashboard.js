/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard-item/dashboard-item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.actionService = useService("action");
        this.display = {
            controlPanel: {}
        };
        this.statisticsService = useService("awesome_dashboard.statistics");
        onWillStart(this._fetchStatistics);
    }

    async _fetchStatistics() {
        this.statistics = await this.statisticsService.fetchStatistics();
    }

    _openKanbanViewAllCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }

    _openLeads() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
