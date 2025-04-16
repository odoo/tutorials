/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { onWillStart, useState } from "@odoo/owl";
import { PieChart } from "./pie_chart/pie_chart";
import { dashboardItems } from "./dashboard_items";
import { dashboardRegistry } from "./dashboard_registry";
import { SettingsDialog } from "./dashboard_settings/dashboard_settings_dialog"

// const STORAGE_KEY = "unchecked_dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem , PieChart };

    setup() {
        this.action = useService("action");

        this.statistics = useService("awesome_dashboard.loadStatistics");

        this.dialog = useService("dialog"); 

        const hiddenItems = JSON.parse(localStorage.getItem("unchecked_dashboard_items")) || [];

        this.allItems = Object.values(dashboardRegistry.getAll()); 

        this.state = useState({
            items: this.allItems.filter(item => !hiddenItems.includes(item.id)) || [], 
            stats: {}
        });

        console.log("Loaded Dashboard Items:", this.state.items); // Debugging

        onWillStart(async () => {
            await this._updateStatistics();
        });
    }

    openSettings() {
        this.dialog.add(SettingsDialog, {
            displayedItems: this.state.items, // ✅ Pass currently displayed items
            onSettingsApplied: () => this._loadDashboardItems(),
        });
    }
    
    async _updateStatistics() {
        if (this.statistics.isReady) {
            this.state.stats = { ...this.statistics };
        }
    }
    
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "kanban"], [false, "list"], [false, "form"]],
            target: "current",
        });
    }

    _loadDashboardItems() {
        const hiddenItems = JSON.parse(localStorage.getItem("unchecked_dashboard_items")) || [];
        this.state.items = Object.values(dashboardRegistry.getAll()).filter(item => !hiddenItems.includes(item.id));
    }
    
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
