import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";


export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };

    static props = {
        items: Array,
        disabledItems: Array,
        onUpdateConfiguration: Function,
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

    _t(...args) {
        return _t(...args);
    }

    onClickDone() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;

        const newDisabledItems = Object.values(this.items)
        .filter((item) => !item.enabled)
        .map((item) => item.id);

        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);

        this.props.onUpdateConfiguration(newDisabledItems);
    }
    
}
