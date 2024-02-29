/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.DashboardDialog";
    static components = { Dialog, CheckBox };

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                checked: !this.props.uncheckedItems.includes(item.id),
            }))
        );
    }

    done() {
        this.props.close();
    }

    onChange(checked, item) {
        item.checked = checked;
        const newUncheckedItems = Object.values(this.items)
            .filter((item) => !item.checked)
            .map((item) => item.id);

        browser.localStorage.setItem("uncheckedItems", newUncheckedItems);
        this.props.updateConfiguration(newUncheckedItems);
    }
}
