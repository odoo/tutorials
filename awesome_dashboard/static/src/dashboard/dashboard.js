/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_items/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { SettingsDialog } from "./settings/settings";
import { dashboardRegistry } from "./dashboard_items/dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, SettingsDialog }

    setup() {
        this.items = dashboardRegistry.getAll();
        this.dialog = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState(this.statisticsService.statistics);
        this.action = useService("action");
        const hiddenItemsList = JSON.parse(localStorage.getItem("hidden_dashboard_items")) ;
        this.state.hidden_dashboard_items = new Set(hiddenItemsList);
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openDialog() {
        this.dialog.add(SettingsDialog, {
            hidden_dashboard_items: [...this.state.hidden_dashboard_items],
            onApply: (hidden_dashboard_items) => {
                this.state.hidden_dashboard_items = new Set(hidden_dashboard_items);
                localStorage.setItem("hidden_dashboard_items", JSON.stringify(hidden_dashboard_items));
            },
        });
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'CRM Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list']],
        });
    }

    get visibleItems() {
        return Object.values(dashboardRegistry.getAll()).filter(item => !this.state.hidden_dashboard_items.has(item.id));
    }


    get display() {
        return {
            controlPanel: {},
        };
    }

}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);