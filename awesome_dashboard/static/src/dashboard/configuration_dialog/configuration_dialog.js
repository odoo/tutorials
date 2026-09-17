import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog };
    static props = {
        items: Array,
        disabledItems: Array,
        close: Function,
        onUpdateConfiguration: Function,
    };

    setup() {
        this.userService = useService("user");
        this.items = this.props.items;
        this.state = useState({});
        for (const item of this.items) {
            this.state[item.id] = !this.props.disabledItems.includes(item.id);
        }
    }

    async done() {
        const disabledItems = Object.keys(this.state).filter((id) => !this.state[id]);
        const jsonSettings = JSON.stringify(disabledItems);
        browser.localStorage.setItem("awesome_dashboard.disabled_items", jsonSettings);
        try {
            await this.userService.setUserSettings("awesome_dashboard.disabled_items", jsonSettings);
        } catch {
            // Fallback to localStorage if res.users.settings field is not extended
        }
        this.props.onUpdateConfiguration(disabledItems);
        this.props.close();
    }
}
