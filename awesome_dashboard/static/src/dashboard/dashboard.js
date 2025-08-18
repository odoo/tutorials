/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
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
        this.orm = useService("orm");
        this.statistics = useState(this.statisticsService.statistics)
        this.itemsState = useState({});
        this.dashboardItems = registry.category("awesome_dashboard").get("awesome_dashboard.dashboard_items");
        onMounted(async () => {
            await this.getConfigSetting();
        })
    }

    async getConfigSetting() {
        const settings = await this.orm.call("res.config.settings", "get_values")
        const settingsFormatted = Object.entries(settings).reduce((acc, [key, val]) => {
            acc = { ...acc, [key]: !!val };
            return acc;
        });
        Object.assign(this.itemsState, settingsFormatted);
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
            items: this.dashboardItems,
            itemsState: this.itemsState,
        })
    }

    openSettings() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Settings',
            res_model: 'res.config.settings',
            views: [[false, 'form']],
            target: 'new',
            context: "{ 'module': 'awesome_dashboard' }"
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard_component", AwesomeDashboard);
