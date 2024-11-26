/** @odoo-module **/

import {Component, useState, toRaw} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import {Dialog} from "@web/core/dialog/dialog";
import {CheckBox} from "@web/core/checkbox/checkbox";
import {browser} from "@web/core/browser/browser";
import {DashboardItem} from "./dashboard_item";
import {NumberCard} from "./card/number_card";
import {PieCard} from "./card/pie_card";

const DISABLED_STORAGE_KEY = "awesome_dashboard.disabledItems"

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, NumberCard, PieCard};

    setup() {
        this.action = useService("action");
        this.items = registry.category("awesome_dashboard_items").getAll();
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialogService = useService("dialog");

        const storedDisabledItems = browser.localStorage.getItem(DISABLED_STORAGE_KEY)
        this.state = useState({disabledItems: storedDisabledItems ? JSON.parse(storedDisabledItems) : []})
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("All leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openSettings() {
        this.dialogService.add(SettingDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateSettings: this.updateSettings.bind(this),
        })
    }

    updateSettings(disabledItems) {
        browser.localStorage.setItem(DISABLED_STORAGE_KEY, JSON.stringify(disabledItems));
        this.state.disabledItems = disabledItems;
    }
}


class SettingDialog extends Component {

    static template = "awesome_dashboard.SettingDialog";
    static components = {Dialog, CheckBox};

    static props = {
        items: {type: Array},
        disabledItems: {type: Array},
        onUpdateSettings: {type: Function},
    }

    setup() {
        const items = this.props.items.map(item => ({
            ...item,
            disabled: this.props.disabledItems.includes(item.id),
        }));
        this.items = useState(items);
        this.onCheckBoxChange = this.onCheckBoxChange.bind(this);
    }

    onCheckBoxChange(item) {
        item.disabled = !item.disabled;
    }

    onDone() {
        const disabledItems = this.items.filter(item => item.disabled).map(item => item.id);
        this.props.onUpdateSettings(disabledItems);
        this.props.close();
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
