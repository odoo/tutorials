/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { configurationDialog } from "./configuration_dialog";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useState(useService("statistics_service"));
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
        this.items = registry.category("dashboard_items").getAll();
        onWillStart(async () => {
            this.result = await this.statistics.loadStatistics();
        });
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list', 'form']],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    actualizeDisplayedItems(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    openControlPanel() {
        this.dialog.add(configurationDialog, {
            items: this.items,
            close: null,
            onConfirm: this.actualizeDisplayedItems.bind(this),
            disabledItems: this.state.disabledItems,
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
