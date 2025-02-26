/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry, Registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { NumberCard } from "../item/numbercard";
import { PieChartCard } from "../item/piechartcard";
import { items } from "./dashboard_items";

export const awesome_dashboard = new Registry("awesome_dashboard");

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, NumberCard, PieChartCard };

    async setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));

        awesome_dashboard.getEntries().forEach(([key]) => {
            awesome_dashboard.remove(key);
        });
        this.cardsState = JSON.parse(browser.sessionStorage.getItem("awesome_dashboard.cards_state"));
        for (var i = 0, item; item = items[i]; i++) {
            if (this.cardsState) {
                item.active = this.cardsState[i];
            }
            awesome_dashboard.add(item.id, item);
        }
        this.items = awesome_dashboard.getAll();
    }

    async openPartners() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    async openSettings() {
        this.dialog.add(SettingsDialog, {
            items: this.items
        })
    };

}

export class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        items: Object
    };

    saveSettings(items) {
        let states = [];
        for (var i = 0, item; item = this.props.items[i]; i++) {
            states.push(item.active);
        }
        browser.sessionStorage.setItem("awesome_dashboard.cards_state", JSON.stringify(states));
        this.props.close();
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
