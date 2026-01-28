import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { browser } from "@web/core/browser/browser";
import { ConfigurationDashboard } from "./configuration_dashboard";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {
        Layout,
        DashboardItem,
    };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);

        const storedConfig = browser.localStorage.getItem("disabledDashboardItems");
        this.state = useState({
            disabledItems: storedConfig ? JSON.parse(storedConfig) : [],
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
        });
    }
    get filteredItems() {
        const allItems = registry.category("dashboard_items").getAll();
        return allItems.filter((item) => !this.state.disabledItems.includes(item.id));
    }
    openConfiguration() {
        this.dialog.add(ConfigurationDashboard, {
            items: registry.category("dashboard_items").getAll(),
            disabledItems: this.state.disabledItems,
            onApply: (disabledItems) => {
                this.state.disabledItems = disabledItems;
                browser.localStorage.setItem("disabledDashboardItems", JSON.stringify(disabledItems));
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
