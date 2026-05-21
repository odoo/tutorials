import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";


export class DialogComponent extends Component {
    static template = "awesome_dashboard.dialog"

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: this.props.disabledItems.includes(item.id),
            }
        }));
    }

    onChange(item, el) {
        item.enabled = el.target.checked

        const newDisabledItems = []

        for (const i of this.items) {
            if (i.enabled) newDisabledItems.push(i.id)

        }
        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems.join(','),
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }
    onApply() {
        this.props.close();
    }

    static components = { Dialog }
}