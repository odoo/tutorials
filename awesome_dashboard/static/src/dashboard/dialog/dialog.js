import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

export class MyDialog extends Component {
    static template = "awesome_dashboard.MyDialog";
    static components = { Dialog };
    static props = ["close", "items", "onApply"];

    setup() {
        const saved = JSON.parse(browser.localStorage.getItem("dashboard_removed_items") || "[]");

        this.selectedState = useState({});

        for (const item of this.props.items) {
            this.selectedState[item.id] = !saved.includes(item.id);
        }
    }

    onChange(ev, itemId) {
        this.selectedState[itemId] = ev.target.checked;
    }

    apply() {
        const removedIds = Object.entries(this.selectedState)
            .filter(([id, checked]) => !checked)
            .map(([id]) => id);

        browser.localStorage.setItem("dashboard_removed_items", JSON.stringify(removedIds));

        if (this.props.onApply) {
            this.props.onApply();
        }

        this.props.close();
    }
}
