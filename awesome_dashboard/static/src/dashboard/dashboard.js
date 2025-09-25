/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { browser } from "@web/core/browser/browser";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({ itemsNotShown: browser.localStorage.getItem("itemsNotShown")?.split(",") || []});
    }

    openPartners() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('All Leads'),
            res_model: 'crm.lead',
            views: [
                [false, 'list'], 
                [false, 'form']
            ],
        });
    }

    openSettingsDialog() {
        this.dialog.add(SettingsDialog, {
            items: this.items,
            dashboard: this,
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);

class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog, CheckBox };
    static props = ["dashboard", "items"];

    setup() {
        this.items = useState(this.props.items);
        this.items.forEach((item) => { item.shown = !this.props.dashboard.state.itemsNotShown.includes(item.id)});
    }

    toggleItem (ev, item) {
        item.shown = ev;

        const newItemsNotShown = Object.values(this.items)
            .filter((i) => !i.shown)
            .map((i) => i.id)

        browser.localStorage.setItem("itemsNotShown", newItemsNotShown);

        this.props.dashboard.state.itemsNotShown = newItemsNotShown;
    }
}