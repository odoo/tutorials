/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.DashboardSettings";
    static components = { Dialog };

    static props = {
        close: { type: Function },
    };

    setup() {
        const items = this.props.items || {};
        const initialUncheckedItems = this.props.initialUncheckedItems || [];

        this.dialogDisplayItems = useState(
            Object.values(items).map((item) => ({
                ...item,
                checked: !initialUncheckedItems.includes(item.id),
            }))
        );
    }

    onChange(checked, itemInDialog) {
        const targetItem = this.dialogDisplayItems.find(i => i.id === itemInDialog.id);
        if (targetItem) {
            targetItem.checked = checked;
        }
    }

    confirmChanges() {
        const newUncheckedItems = this.dialogDisplayItems.filter((item) => !item.checked).map((item) => item.id);

        browser.localStorage.setItem("uncheckedItems", newUncheckedItems.join(","));

        if (this.props.updateConfiguration) {
            this.props.updateConfiguration(newUncheckedItems);
        }
        this.props.close();
    }
}
