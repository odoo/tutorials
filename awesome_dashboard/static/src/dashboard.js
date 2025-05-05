/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticStateService = useService("statistics_service");
        this.result = useState(this.statisticStateService.loadStatisticsRealTime());

        /// Other methods of retrieving data: rpc call every time & memoize rpc call
        // onWillStart(async () => {
            // this.result = await this.statisticStateService.loadStatisticsRPC();
            // this.result = await this.statisticStateService.loadStatistics();
        // });
    }

    openCustomersKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'res.partner',
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
