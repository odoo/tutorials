/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";

import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";

import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.statistics = useState(useService("statistics"));
        this.dialog = useService("dialog");
        this.dashboardItems = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            visibleItems: browser.localStorage.getItem("visibleItems") || [],
        });
        if (!this.state.visibleItems.length) {
            this.state.visibleItems = this.dashboardItems.map((item) => item.id);
            browser.localStorage.setItem("visibleItems", this.state.visibleItems);
        }
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("CRM Leads"),
            target: "current",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openSettings() {
        this.dialog.add(SettingsDialog, {
            items: this.dashboardItems,
            visibleItems: this.state.visibleItems,
            onUpdateSettings: this.updateSettings.bind(this),
        });
    }

    updateSettings(updatedVisibleItems) {
        this.state.visibleItems = updatedVisibleItems;
    }
}

class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "visibleItems", "onUpdateSettings"];

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                visible: this.props.visibleItems.includes(item.id),
            }))
        );
    }
    closeDialog() {
        this.props.close();
    }

    onChange(ev, settingItem) {
        settingItem.visible = ev;
        const updatedItems = this.items.filter((item) => item.visible).map((item) => item.id);
        browser.localStorage.setItem("visibleItems", updatedItems);

        this.props.onUpdateSettings(updatedItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
