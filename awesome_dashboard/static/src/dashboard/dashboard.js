/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./Dashboard_item/Dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, Dialog }

    async setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").get("dashboard_items");
        this.dialog = useService("dialog");

        this.state = useState({
            disabledItems:
                browser.localStorage.getItem("uncheckedItems")?.split(",") || [],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

    openConfigurations() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfigurations: this.updateConfigurations.bind(this),
        })
    }

    updateConfigurations(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfigurations"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    apply() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        console.log(changedItem, checked);
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );
        console.log(browser.localStorage.getItem("disabledDashboardItems"));
        this.props.onUpdateConfigurations(newDisabledItems);
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
