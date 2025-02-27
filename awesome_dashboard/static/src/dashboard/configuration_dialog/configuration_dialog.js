/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.configuration_dialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => ({
            ...item,
            enabled: !this.props.disabledItems.includes(item.id),
        })));
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
    }

    done() {
        const newDisabledItems = this.items
            .filter(item => !item.enabled)
            .map(item => item.id);
        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);
        this.props.onUpdateConfiguration(newDisabledItems);
        this.props.close();
    }
}
