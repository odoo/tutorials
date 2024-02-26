/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import { DashboardItem } from "./dashboard_item";

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

import {_lt} from "@web/core/l10n/translation"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = {
            controlPanel: {} 
        };
        this.dialog = useService("dialog");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.action = useService("action");
        this._lt = _lt;
        this.userService = useService('user');

        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: JSON.parse(this.userService.settings.disabled_items)
        });
    }       

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    onClickBtnCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    onClickBtnLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.userService = useService('user');
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

        this.userService.setUserSettings("disabled_items", JSON.stringify(newDisabledItems));

        this.props.onUpdateConfiguration(newDisabledItems);
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
