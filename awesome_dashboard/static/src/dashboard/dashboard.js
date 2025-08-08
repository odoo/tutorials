
import { Component, onWillStart, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService, useBus } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./components/pie_chart";
import { _t } from "@web/core/l10n/translation";
import { SettingDialog } from "./setting/dashboard_settings";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, SettingDialog};
    static props = {};
    setup() {
        this.action = useService("action");
        this.dialogService = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);
        //const itemsRegistry = registry.category("awesome_dashboard_items");
        //this.allItems = itemsRegistry ? itemsRegistry.getAll() : []; 

        this.state = useState({
            hiddenItems: this.getHiddenItems(),
            // visibleItems: [],
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
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    getHiddenItems() {
        return JSON.parse(localStorage.getItem("awesome_dashboard_hidden_items")) || [];
    }

    getFilteredItems() {
        const hiddenSet = new Set(this.state.hiddenItems);
        return registry.category("awesome_dashboard_items").getAll().filter(item => !hiddenSet.has(item.id));
    }

    openSettings() {
        this.dialogService.add(SettingDialog, {
            onApply: (hiddenItems) => {
                console.log("Dashboard onApply callback, hidden items:", hiddenItems);
                localStorage.setItem("awesome_dashboard_hidden_items", JSON.stringify(hiddenItems));
                this.state.hiddenItems = hiddenItems;
            }
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
