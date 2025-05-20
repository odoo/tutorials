import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

export class ConfigurationDialog extends Component {
    static template = 'awesome_dashboard.ConfigurationDialog';
    static components = { Dialog };
    static props = {
        title: String,
        message: String,
        items: Array,
        disabledItems: Array,
        onUpdateConfiguration: Function,
        close: Function
    };

    setup() {
        this.items = useState(this.props.items.map((item) => ({
            ...item,
            enabled: !this.props.disabledItems.includes(item.id),
        })));
    }

    apply() {
        const newDisabledItems = Object.values(this.items)
        .filter(item => !item.enabled)
        .map(item => item.id);

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems
        );

        this.props.onUpdateConfiguration(newDisabledItems);
        this.props.close();
    }

    onChange(state, changedItem) {
        changedItem["enabled"] = state;
    }
}
