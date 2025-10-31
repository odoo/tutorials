/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { DashboardSettingsDialog } from "./dashboard_settings_dialog";
 
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dashboardRegistry = registry.category("awesome_dashboard.items");
        this.display = {
            controlPanel: {},
        };
        this.state = useState({
            items: this.getVisibleItems()
        });
    }

    getVisibleItems() {
        const allItems = this.dashboardRegistry.getAll();
        const hiddenItems = this.getHiddenItems();
        return allItems.filter(item => !hiddenItems.includes(item.id))
    }

    getHiddenItems() {
        const stored = localStorage.getItem('dashboard_hidden_items');
        return stored ? JSON.parse(stored) : [];
    }

    saveHiddenItems(hiddenItemIds){
        localStorage.setItem('dashboard_hidden_items', JSON.stringify(hiddenItemIds));
        this.state.items = this.getVisibleItems();
    }

    openSettings() {
        const allItems = this.dashboardRegistry.getAll();
        this.dialog.add(DashboardSettingsDialog, {
            items: allItems,
            hiddenItems: this.getHiddenItems(),
            onApply: (hiddenItemIds) => {
                this.saveHiddenItems(hiddenItemIds);
            }
        })
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);