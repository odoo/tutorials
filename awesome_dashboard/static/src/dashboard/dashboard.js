import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = {
            controlPanel: {},
        }
        this.action = useService("action");
        this.userService = useService("user");
        const statisticsService = useService("awesome_dashboard.statistics");
        this.stats = useState(statisticsService);
        this.dialog = useService("dialog");

        const savedSettings = this.userService.settings["awesome_dashboard.disabled_items"] || browser.localStorage.getItem("awesome_dashboard.disabled_items");
        const disabledItems = savedSettings ? JSON.parse(savedSettings) : [];
        this.state = useState({ disabledItems });
    }

    get items() {
        return registry.category("awesome_dashboard").getAll().filter(
            (item) => !this.state.disabledItems.includes(item.id)
        );
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: registry.category("awesome_dashboard").getAll(),
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: (newDisabledItems) => {
                this.state.disabledItems = newDisabledItems;
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
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
