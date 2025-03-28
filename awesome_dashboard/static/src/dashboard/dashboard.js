/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        
        this.items = registry.category("awesome_dashboard").getAll();

        this.statistics = useState(useService("awesome_dashboard.statistics"));
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('All leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
