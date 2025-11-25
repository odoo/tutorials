/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { rpc } from "@web/core/network/rpc";

export class DashboardSetting extends Component {
    static template = "awesome_dashboard.setting";
    static components = { Dialog };
    static props = {
        close: { type: Function },
    };
    setup() {
        const items = this.props.items || {};
        const initialDisabledItems = this.props.initialDisabledItems || [];
        this.settingDisplayItems = Object.values(items).map((item) => ({
            ...item,
            checked: !initialDisabledItems.includes(item.id),
        }));
    }

    onChange(checked, itemInDialog) {
        const targetItem = this.settingDisplayItems.find(i => i.id === itemInDialog.id);
        if (targetItem) {
            targetItem.checked = checked;
        }
    }

    async confirmDone() {
        const newDisableItems = this.settingDisplayItems.filter((item) => !item.checked).map((item) => item.id);
        await rpc("/web/dataset/call_kw/res.users/set_dashboard_settings", {
            model: 'res.users',
            method: 'set_dashboard_settings',
            args: [newDisableItems],
            kwargs: {},
        });
        if (this.props.updateSettings) {
            this.props.updateSettings(newDisableItems);
        }
        this.props.close();
    }
}
