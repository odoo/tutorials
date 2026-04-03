/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.DashboardSettings";

    static props = {
        items: Array,
        removed: { type: Array, optional: true },
        onApply: Function,
        close: Function,
    };

    setup() {
        this.state = useState({
            removed: this.props.removed ? [...this.props.removed] : [],
        });
    }

    // ✅ checkbox state
    isChecked(id) {
        return !this.state.removed.includes(id);
    }

    // ✅ toggle items
    toggleItem(id, ev) {
        const checked = ev.target.checked;

        if (!checked) {
            if (!this.state.removed.includes(id)) {
                this.state.removed.push(id);
            }
        } else {
            this.state.removed = this.state.removed.filter(
                (i) => i !== id
            );
        }
    }

    // ✅ APPLY (SAVE TO SERVER)
    async apply() {
        try {
            await rpc("/awesome_dashboard/save_config", {
                config: JSON.stringify(this.state.removed),
            });

            this.props.onApply(this.state.removed);
            this.props.close();
        } catch (e) {
            console.error("Failed to save dashboard config:", e);
        }
    }

    close() {
        this.props.close();
    }
}
