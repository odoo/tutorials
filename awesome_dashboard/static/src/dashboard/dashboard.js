
import { Component, useState } from "@odoo/owl";

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { PieChart } from "./pie_chart/pieChart"
import { DashboardItem } from "./dashboard_item/dashboardItem";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
    }

    customerButtonClick() {
        this.action.doAction("base.action_partner_form");
    }

    leadsButtonClick() {
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

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
