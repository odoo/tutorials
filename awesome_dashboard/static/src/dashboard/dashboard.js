/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./piechart/piechart";
import { ItemsDialog } from "./dialog/items_dialog";
import { browser } from "@web/core/browser/browser";
import { useStatistics } from "./statistics";
import { useDashboardItems } from "./dashboard_items";

class AwesomeDashboard extends Component {
    setup() {
        this.items = useDashboardItems();

        this.action = useService("action");
        this.dialog = useService("dialog");

        this.statistics = useStatistics();
        this.state = useState({
            currentVisibleItems: this.getVisibleItems(),
        });
    }

    getVisibleItems() {
        const localStorageItems = JSON.parse(browser.localStorage.getItem("invisibleItemIds")) || [];
        return this.items.filter((item) => !localStorageItems.includes(item.id));
    }

    updateVisibleItems() {
        this.state.currentVisibleItems = this.getVisibleItems();
    }

    openDialog() {
        this.dialog.add(ItemsDialog, {
            items: this.items,
            apply: () => {
                this.updateVisibleItems();
            },
        });
    }

    async openCustomersKanban() {
        await this.action.doAction("base.action_partner_form");
    }

    async openCrmLeads() {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "tree"]],
            target: "current",
        });
    }
}

AwesomeDashboard.template = "awesome_dashboard.AwesomeDashboard";
AwesomeDashboard.components = { Layout, DashboardItem, PieChart, DialogItems: ItemsDialog };

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
