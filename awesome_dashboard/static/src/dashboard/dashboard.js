/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems:
                browser.localStorage
                    .getItem("disabledDashboardItems")
                    ?.split(",") || [],
        });
        this.openSettings = this.openSettings.bind(this);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            name: "Leads",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openSettings() {
        this.dialog.add(SettingsDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateSettings: this.updateSettings.bind(this),
            close: this.closeSettings.bind(this),
        });
    }

    updateSettings(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    closeSettings() {
        this.dialog.close();
    }
}

class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: Array,
        disabledItems: Array,
        onUpdateSettings: Function,
        close: Function,
    };

    setup() {
        this.items = useState(
            this.props.items.map((item) => {
                return {
                    ...item,
                    enabled: !this.props.disabledItems.includes(item.id),
                };
            })
        );
    }

    closeDialog() {
        this.props.close();
    }

    onChange(chekced, changedItem) {
        changedItem.enabled = chekced;
        const newDisabledItems = Object.values(this.items)
            .filter((item) => !item.enabled)
            .map((item) => item.id);

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems
        );

        this.props.onUpdateSettings(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
