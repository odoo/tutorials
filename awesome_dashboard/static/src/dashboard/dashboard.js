/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action")
        this.dialog = useService("dialog")
        this.statistics = useState(useService("awesome_dashboard.statistics"))
        this.items = registry.category("awesome_dashboard").getAll()
        this.state = useState({ disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || [] })
    }

    async openCustomers() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'res.partner',
            views: [[false, 'kanban']],
        });
    }

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            name: 'Leads',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    async openConfiguration() {
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

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog"
    static components = { Dialog, CheckBox }
    static props = ["close", "items", "disabledItems"]

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return { ...item, enabled: !this.props.disabledItems.includes(item.id)}
        }))
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

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
