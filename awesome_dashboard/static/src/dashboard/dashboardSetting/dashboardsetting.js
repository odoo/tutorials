/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class DashboardSetting extends Component {
    static template = "awesome_dashboard.setting";

    static components = { Dialog };

    static props = {
        close: { type: Function }
    };

    setup() {
        const items = this.props.items || {};
        const initialDisabledItems = this.props.initialDisabledItems || [];
        this.settingDisplayItems = Object.values(items).map((item) => ({
            ...item,
            checked: !initialDisabledItems.includes(item.id),
        }))
    }

    _t(...args) {
        return _t(...args);
    }

    onChange(checked, itemInDialog) {
        const targetItem = this.settingDisplayItems.find(i => i.id === itemInDialog.id);
        if (targetItem) {
            targetItem.checked = checked;
        }
    }

    async confirmDone() {
        const newDisableItems = this.settingDisplayItems.filter((item) => !item.checked).map((item) => item.id);
        if (this.props.updateSettings) {
            this.props.updateSettings(newDisableItems);
        }
        this.props.close();
    }
}
