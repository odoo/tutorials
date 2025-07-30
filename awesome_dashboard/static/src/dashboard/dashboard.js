/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "../dashboard-item/dashboard_item";
import { PieChart } from "../piechart/piechart";
import { DashboardDialog } from "../dashboard_dialog/dashboard_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics)
        this.itemsState = useState(this.statisticsService.itemsState);
        this.dashboardItems = registry.category("awesome_dashboard").get("awesome_dashboard.dashboard_items");
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openConfigurationDialog() {
        this.dialog.add(DashboardDialog, {
            items: this.dashboardItems
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard_component", AwesomeDashboard);
