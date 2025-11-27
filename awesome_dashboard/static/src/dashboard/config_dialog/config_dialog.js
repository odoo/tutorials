/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog };
    static props = {
        close: Function,
    };

    setup() {
        this.user = useService("user");
        this.items = registry.category("awesome_dashboard").getEntries().map(([id, item]) => ({
            id,
            description: item.description,
            enabled: !this.getDisabledItems().includes(id),
        }));
        this.state = useState({ items: this.items });
    }

    getDisabledItems() {
        return this.user.settings?.awesome_dashboard_disabled_items || [];
    }

    toggleItem(item) {
        item.enabled = !item.enabled;
    }

    async save() {
        const disabledItems = this.state.items
            .filter((item) => !item.enabled)
            .map((item) => item.id);
        
        await this.user.setUserSettings("awesome_dashboard_disabled_items", disabledItems);
        window.location.reload(); 
    }
}
