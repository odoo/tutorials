/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout';
import { useService } from '@web/core/utils/hooks'
import { DashboardItem } from "@awesome_dashboard/dashboaed_item";
import { PieChart } from "@awesome_dashboard/pie_chart/pie_chart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart}

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics")

        onWillStart(async () => {
            this.statistics = await this.statistics.loadStatistics();
        })
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
