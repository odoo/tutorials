import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { browser } from "@web/core/browser/browser";
import { ConfigurationDialog } from "./configuration_dialog";
import { DashboardItem } from "./dashboardItem";

const STORAGE_KEY = "awesome_dashboard.disabled_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialog = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({ disabledItems: this.loadDisabledItems() });
    }

    loadDisabledItems() {
        try {
            return JSON.parse(browser.localStorage.getItem(STORAGE_KEY)) || [];
        } catch {
            return [];
        }
    }

    get visibleItems() {
        return this.items.filter((item) => !this.state.disabledItems.includes(item.id));
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onApply: (disabledItems) => {
                browser.localStorage.setItem(STORAGE_KEY, JSON.stringify(disabledItems));
                this.state.disabledItems = disabledItems;
            },
        });
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form");
    }

    openLead() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
