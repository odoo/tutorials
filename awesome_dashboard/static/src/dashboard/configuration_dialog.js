/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class configurationDialog extends Component {
    static template = "awesome_dashboard.configuration_dialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: Object,
        close: Function,
        onConfirm: Function,
        disabledItems: Object,
    };

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                is_displayed: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    toggleState(checked, changedItem) {
        changedItem.is_displayed = checked;
        const newDisabledItems = Object.values(this.items).filter((item) => !item.is_displayed).map((item) => item.id)
        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems,);
    }

    apply() {
        const newDisabledItems = Object.values(this.items).filter((item) => !item.is_displayed).map((item) => item.id)
        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems,);
        this.props.onConfirm(newDisabledItems);
    }
    
    closeAndApply() {
        this.apply();
        this.props.close();
    }
}
