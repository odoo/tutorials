import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { dashboardItemRegistry } from "./dashboard_registry";
import { DashboardSettingsDialog } from "./dashboard_settings_dialog";

const STORAGE_KEY = "awesome_dashboard_removed_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {
        Layout,
        DashboardItem,
        PieChart,
        NumberCard,
        PieChartCard,
    };

    setup() {
        this.action = useService("action");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));
        this.dialogService = useService("dialog");

        this.state = useState({
            removedItems: this.loadRemovedItems(),
        });

        onWillStart(async () => {
            await this.statisticsService.loadStatistics();
        });

        this.items = dashboardItemRegistry.getAll();
    }

    loadRemovedItems() {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    }

    saveRemovedItems(ids) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
        this.state.removedItems = ids;
    }

    sanitizeProps(props) {
        const clean = { ...props };
        delete clean.slots;
        return clean;
    }

    get visibleItems() {
        return this.items.filter(
            (item) => !this.state.removedItems.includes(item.id)
        );
    }

    openSettings() {
        this.dialogService.add(DashboardSettingsDialog, {
            items: this.items,
            removedItems: this.state.removedItems,
            onApply: (removedIds) => {
                this.saveRemovedItems(removedIds);
            },
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() { 
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);