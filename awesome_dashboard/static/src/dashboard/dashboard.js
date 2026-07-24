import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";


import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart";

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

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statService = useService("statistics");
        this.statistics = this.statService.onUpdate;
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            // NOTE; ConfigurationDialog performs saving into browser local storage
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || [],
        })

        onWillStart(async () => {
            const result = await this.statService.loadStatistics();
            // WARN; Perform immediate/synchronous update of state because sub-components
            // logic isn't safeguarded against undefined values.
            for (const [key, value] of Object.entries(result)) {
                this.statistics[key] = value;
            }
        });
    }

    async openCustomers() {
        this.action.doAction("base.action_partner_form", {});
    }

    async openLeads() {
        this.action.doAction("crm.crm_lead_all_leads");
    }

    async openSettings() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    async updateConfiguration(newDisabledItems) { 
        this.state.disabledItems = newDisabledItems; 
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
