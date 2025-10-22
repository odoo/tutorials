import { Component, reactive, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { DashboardItemsDialog } from "./dashboard_items_dialog/dashboard_items_dialog";

const EXCLUDED_DASHBOARD_ITEMS_LS_KEY = 'excluded_dashboard_items';

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, DashboardItemsDialog, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");

        this.statisticsService = useService("statistics");
        this.state = useState(this.statisticsService);

        this.items = registry.category('dashboard_items').getAll();
        useBus(registry.category('dashboard_items'), 'UPDATE', this.handleDashboardItemsUpdate.bind(this));

        const initExcludedItems = JSON.parse(localStorage.getItem(EXCLUDED_DASHBOARD_ITEMS_LS_KEY)) ?? [];
        const storedStateObj = { excludedItems: initExcludedItems };
        const store = obj => localStorage.setItem(EXCLUDED_DASHBOARD_ITEMS_LS_KEY, JSON.stringify(obj.excludedItems));
        const reactiveStoredState = reactive(storedStateObj, () => store(reactiveStoredState));
        store(reactiveStoredState);
        this.storedState = useState(storedStateObj);
    }

    handleDashboardItemsUpdate(event) {
        this.items = registry.category('dashboard_item').getAll();
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

    handleDashboardItemsConfigChange(excludedItems) {
        this.storedState.excludedItems = excludedItems;
    }

    openSettings() {
        this.removeSettingsDialog = this.dialog.add(DashboardItemsDialog, {
            items: this.items,
            excludedItems: this.storedState.excludedItems,
            onApply: this.handleDashboardItemsConfigChange.bind(this),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
