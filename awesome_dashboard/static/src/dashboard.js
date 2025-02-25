
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { Component, useState } from "@odoo/owl";

import { DashboardItem } from "./item/dashboardItem";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
    }

    onCustomerButtonClick(buttonName) {
        this.action.doAction("base.action_partner_form");
    }

    onLeadsButtonClick(buttonName) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('action_partner_form'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            search_view_id: [false],
            domain: [],
        });
    }
    
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
