/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

const LS_KEY = "awesome_dashboard.removed_items";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };
    static props = {
        items: { type: Array },
        removedIds: { type: Array },
        close: { type: Function },
        onApply: { type: Function, optional: true },
    };

    setup() {
        const checkedById = {};
        const removedSet = new Set(this.props.removedIds || []);
        for (const item of this.props.items) {
            checkedById[item.id] = !removedSet.has(item.id);
        }
        this.state = useState({ checkedById });
    }

    toggle(id) {
        this.state.checkedById[id] ^= 1; // style points ;)
    }

    apply() {
        const removed = this.props.items
            .filter((it) => !this.state.checkedById[it.id])
            .map((it) => it.id);
        window.localStorage.setItem(LS_KEY, JSON.stringify(removed));
        if (this.props.onApply) {
            this.props.onApply(removed);
        }
        this.props.close();
    }
}
