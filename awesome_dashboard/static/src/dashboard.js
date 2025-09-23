/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.action = useService("action");
        this.stats = useService("awesome_dashboard.statistics").getStatistics()
    }
    openPartners() {
        this.action.doAction("base.action_partner_form");
    }
    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('All Leads'),
            res_model: 'crm.lead',
            views: [
                [false, 'list'], 
                [false, 'form']
            ],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
