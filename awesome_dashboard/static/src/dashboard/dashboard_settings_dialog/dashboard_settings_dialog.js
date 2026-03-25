import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    done() {
       this.props.close();
    }

    onChange(ev, item) {
        const checked = ev.target.checked;
        item.enabled = checked;
        const newDisabledItems = this.items
            .filter((i) => !i.enabled)
            .map((i) => i.id);

        browser.localStorage.setItem(
            "disabledDashboardItems",
            JSON.stringify(newDisabledItems)
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}
