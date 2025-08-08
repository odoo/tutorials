/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboarditem";
import { DashboardSetting } from "./dashboardSetting/dashboardsetting";
import { PieChart } from "./piechart/piechart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        const dashboardItemsRegistry = registry.category("awesome_dashboard");
        this.items = dashboardItemsRegistry.getAll();
        this.dialogService = useService("dialog");


        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState({ statistics: this.statisticsService.statistics });


        this.displayState = useState({
            disabledItems: [],
        });
    }

    updateSettings(newUncheckedItems) {
        this.displayState.disabledItems.length = 0;
        this.displayState.disabledItems.push(...newUncheckedItems);
    }

    openSettings() {
        this.dialogService.add(DashboardSetting, {
            items: this.items,
            initialDisabledItems: this.displayState.disabledItems,
            updateSettings: this.updateSettings.bind(this),
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeadsView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
