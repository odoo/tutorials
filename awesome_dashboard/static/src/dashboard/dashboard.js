import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";
import { PieChart } from "./piechart";
import { PieChartCard } from "./piechartcard";
import { NumberCard } from "./numbercard";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, NumberCard, PieChartCard };

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.stats);
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.dialog_state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });

        // Shared state usage
        this.sharedState = useService("shared_state");
        this.sharedState.setValue("username", "Tushar");
        console.log(`Hello ${this.sharedState.getValue("username")}`);

        // Action service
        this.action = useService("action");
    }

    updateConfiguration(newDisabledItems) {
        this.dialog_state.disabledItems = newDisabledItems;
    }

    openSetting() {
        this.action.doAction("base_setup.action_general_configuration");
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "current",
            views: [[false, "list"], [false, "form"]],
        });
    }
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.dialog_state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }
}

// Custom Notification Service
const myservices = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 5000);
        return {};
    },
};

// Shared State Service
const sharedStateService = {
    start(env) {
        let state = {};
        return {
            getValue(key) {
                return state[key];
            },
            setValue(key, value) {
                state[key] = value;
            },
        };
    },
};


class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }))
    }

    onDone() {
        this.props.close()
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }

}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
registry.category("services").add("myservices", myservices);
registry.category("services").add("shared_state", sharedStateService);
