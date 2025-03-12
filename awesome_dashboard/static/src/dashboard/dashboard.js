/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup(){
        this.statistic_service = useService("awesome_dashboard.statistics");
        this.result = useState({data: null});
        this.action = useService("action");
        this.result.data = this.statistic_service.stats;
    }

    opoenCustomers(){
        this.action.doAction("base.action_partner_form")
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false,'list'],[false,'form']]
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
