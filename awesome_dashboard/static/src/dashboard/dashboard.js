/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { DashboardSettings } from "./dashboard_settings/dashboard_settings";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.actionService = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);

        this.dialogService = useService("dialog");

        const dashboardItemsRegistry = registry.category("awesome_dashboard");
        this.items = dashboardItemsRegistry.getAll();

        this.state = useState({
            uncheckedItems: browser.localStorage.getItem("uncheckedItems")?.split(",").filter(id => id) || [],
        });
    }

    updateConfiguration(newUncheckedItems) {
        this.state.uncheckedItems.length = 0;
        this.state.uncheckedItems.push(...newUncheckedItems); 
    }

    openConfiguration() {
        this.dialogService.add(DashboardSettings, {
            items: this.items,
            initialUncheckedItems: this.state.uncheckedItems, 
            updateConfiguration: this.updateConfiguration.bind(this),
        });
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
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
