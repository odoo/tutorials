import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../DashboardItem/dashboarditem";
import { DashboardSettings } from "../DashboardSettings/dashboardsettings";
import "../dashboard_items";

const STORAGE_KEY = "awesome_dashboard.removed_item_ids";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.allItems = registry.category("awesome_dashboard").getAll();
        this.actionService = useService("action");
        this.dialogService = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        this.state = useState({
            removedItemIds: this.loadRemovedItemIds(),
        });
    }

    loadRemovedItemIds() {
        try {
            const value = localStorage.getItem(STORAGE_KEY);
            const parsed = value ? JSON.parse(value) : [];
            return Array.isArray(parsed) ? parsed : [];
        } catch (error) {
            console.error("Failed to load removed item ids from localStorage:", error);
            return [];
        }
    }

    saveRemovedItemIds(removedItemIds) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(removedItemIds));
            this.state.removedItemIds = removedItemIds;
        } catch (error) {
            console.error("Failed to save removed item ids to localStorage:", error);
        }
    }

    get items() {
        const removedIds = new Set(this.state.removedItemIds);
        return this.allItems.filter((item) => !removedIds.has(item.id));
    }

    openCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }

    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openSettings() {
        this.dialogService.add(DashboardSettings, {
            title: "Dashboard settings",
            removedItemIds: this.state.removedItemIds,
            applyConfiguration: (removedItemIds) => this.saveRemovedItemIds(removedItemIds),
        });
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
