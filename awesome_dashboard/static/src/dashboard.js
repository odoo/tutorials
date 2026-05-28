import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Layout } from "@web/search/layout"
import { PieChart } from "./pie_chart/pie_chart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.state = useState({
            stats: useService("awesome_dashboard.statistics"),
        });
    }

    async openCustomersKanban() {
        this.action.doAction('base.action_partner_form');
    }

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Lots of Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
