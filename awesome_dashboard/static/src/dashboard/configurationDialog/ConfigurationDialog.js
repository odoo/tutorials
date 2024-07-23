/** @odoo-module */

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };

    setup() {
        console.log(this.props);
    }

    onChange(checked, changedItem) {
        changedItem.disabled = checked;
        const newDisabledItems = Object.values(this.props.items)
            .filter((item) => item.disabled)
            .map((item) => item.id);

        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);
    }

    done() {
        this.props.close();
    }
}
