/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardConfigDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigDialog";
    static components = { Dialog, CheckBox }
    static props = ["close", "items", "disablesItems", "updateConfiguration"]

    setup(){
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disablesItems.includes(item.id)
            }
        }))
    }

    onChange(checked, item) {
        item.enabled = checked;
    }
    
    apply() {
        const newDisabledItems = Object.values(this.items).filter((item) => !item.enabled).map((item) => item.id);

        browser.localStorage.setItem(
            "disabledItems",
            newDisabledItems,
        );

        this.props.updateConfiguration(newDisabledItems);
        this.props.close();
    }
}
