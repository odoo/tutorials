/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboardItem";
import { PieChart } from "./components/PieChart";
import { SettingDialog } from "./setting/setting_dialog";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };
    static props = {}

    setup() {
        this.dialogService = useService("dialog");
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);

        // Use reactive state for hidden items
        this.state = useState({
            hiddenItems: this.getHiddenItems(),
        });

        onWillStart(async () => {
            await this.statisticsService.loadStatistics();
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
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    // Retrieve hidden item IDs from localStorage
    getHiddenItems() {
        return JSON.parse(localStorage.getItem("awesome_dashboard_hidden_items")) || [];
    }

    // Compute filtered items based on hidden items
    getFilteredItems() {
        const hiddenSet = new Set(this.state.hiddenItems);
        return registry.category("awesome_dashboard.items").getAll().filter(item => !hiddenSet.has(item.id));
    }

    openSettings() {
        this.dialogService.add(SettingDialog, {
            onApply: (hiddenItems) => {
                localStorage.setItem("awesome_dashboard_hidden_items", JSON.stringify(hiddenItems));
                this.state.hiddenItems = hiddenItems;
            }
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
