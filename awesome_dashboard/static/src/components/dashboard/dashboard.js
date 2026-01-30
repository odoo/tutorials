import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";
import { DashboardChart } from "./chart/chart";
import { LazyComponent } from "@web/core/assets";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, DashboardChart, LazyComponent };
    
    setup() {
        let savedDisabledItems = [];
        try {
            const rawValue = browser.localStorage.getItem("disabledDashboardItems");
            // Only parse if the value exists
            savedDisabledItems = rawValue ? JSON.parse(rawValue) : [];
        } catch (e) {
            console.error("Failed to parse local storage, resetting to empty array");
            savedDisabledItems = [];
        }

        this.state = useState({
            controlPanel: {},
            disabledItems: savedDisabledItems,
        });

        this.items = registry.category("awesome_dashboard").getAll();
        this.action = useService("action");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));
        console.log("Statistics:", this.statisticsService);
        this.state.result = this.statisticsService;
        this.dialog = useService("dialog");

    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views : [
                [false, "list"],
                [false, "form"]
            ],});
    }
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }
    updateConfiguration(newdisabledItems) {
        this.state.disabledItems = newdisabledItems;
    }
}

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
        }));
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newdisabledItems = Object.values(this.items)
            .filter((item) => !item.enabled)
            .map((item) => item.id);

        // FIX: Wrap the array in JSON.stringify
        browser.localStorage.setItem(
            "disabledDashboardItems",
            JSON.stringify(newdisabledItems) 
        );

        this.props.onUpdateConfiguration(newdisabledItems);
    }
}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
