/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = {
        dashboardItems: Array,
        disabledItems: Array,
        onUpdateConfiguration: Function,
        close: Function
    }

    setup() {
        this.dashboardItems = useState(
            this.props.dashboardItems.map((item) => ({
                ...item,
                isChecked: !this.props.disabledItems.includes(item.id),
            }))
        );

        this.onChange = this.onChange.bind(this);
    }

    onChange(checked, changedItem) {
        changedItem.isChecked = checked;
        const newDisabledItems = Object.values(this.dashboardItems)
        .filter((item) => !item.isChecked)
        .map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }

    done() {
        this.props.close();
    }
}
