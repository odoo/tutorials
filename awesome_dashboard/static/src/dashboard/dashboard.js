/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "../dashboarditem/dashboarditem";
import { Layout } from '@web/search/layout'
import { PieChartCard } from "../cards/piechartcard/piechart";
import { NumberCard } from "../cards/numbercard/numbercard";
import { ItemConfigurationPopup } from "./item_configuration_popup/item_configuration_popup";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const dashboardRegistry = registry.category("awesome_dashboard.dashboard");

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChartCard, NumberCard, ItemConfigurationPopup }
    
    setup() {
        this.action = useService("action");
        this.state = useState({ items: [], chart: {}, itemConfigs: {} });
        this.statisticsService = useService('statistics');
        this.statsResult = useState(this.statisticsService);
        this.dialogService = useService("dialog");
        this.getBrowserLocalStorageData();
    }

    get items() {
        return dashboardRegistry.get("awesome_dashboard.items");
    }

    get chart() {
        return this.statsResult.orders_by_size;
    }

    showDialog() {
        this.updateItemConfig = this.updateItemConfig.bind(this);
        this.closeWrapper = this.closeWrapper.bind(this);
        this.dialogService.add(ItemConfigurationPopup, {
            items: this.items,
            itemConfigs: this.state.itemConfigs,
            closeWrapper: this.closeWrapper,
            updateItemConfigCallback: this.updateItemConfig
        });
    }
    
    openCustomers() {
        this.action.doAction("contacts.action_contacts");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']],    // [view_id, view_type]
        });
    }

    closeWrapper() {
        this.getBrowserLocalStorageData();
    }

    updateItemConfig(updated_itemconfigs) {
        this.state.itemConfigs = updated_itemconfigs;
    }

    getBrowserLocalStorageData() {
        let item_configuration_localdata = browser.localStorage.getItem("awesome_dashboard.item_configuration");
        if (item_configuration_localdata) {
            this.state.itemConfigs = JSON.parse(item_configuration_localdata);
        }
        else {
            let initialToggleState = {};
            for (const item of this.items) {
                initialToggleState[item.id] = true;
            }
            this.state.itemConfigs = initialToggleState;
        }
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
