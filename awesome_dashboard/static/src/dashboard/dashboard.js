// /** @odoo-module **/

import { Layout } from '@web/search/layout';
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { DashboardItem } from './dashboarditem/dashboarditem';
import { PieChart } from './piechart/piechart';
import { NumberCard } from './dashboarditem/numbercard';
import { SettingsDialog } from './settings/settings_dialouge';
import { dashboardRegistry } from './dashboarditem/dashboarditems';

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, NumberCard, PieChart };

    setup(){
        this.action = useService("action")
        this.dialogService = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState(this.statisticsService.state);

        const savedHiddenItems = JSON.parse(localStorage.getItem("hidden_dashboard_items")) || [];
        this.state.hiddenItems = new Set(savedHiddenItems);
    }

    openSettingsDialog() {
        this.dialogService.add(SettingsDialog, {
            onApply: (hiddenItems) => {
                this.state.hiddenItems = new Set(hiddenItems);
                console.log(this.state.hiddenItems)
            },
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form"); 
    }

    openLeads(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: ('Journal Entry'),
            target: 'current',
            res_id: activity.res_id,
            res_model: 'crm.lead',
            views: [[false, 'list']],
        });
    }
    get display(){
        return{
            controlPanel: {} 
        }
    }

    get visibleItems() {
        return Object.values(dashboardRegistry.getAll()).filter(item => !this.state.hiddenItems.has(item.id));
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
