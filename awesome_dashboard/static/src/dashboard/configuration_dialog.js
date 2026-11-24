import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: Array,
        disabledItems: Array,
        onApply: Function,
        close: Function, // injected by the dialog service
    };

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                id: item.id,
                description: item.description,
                enabled: !this.props.disabledItems.includes(item.id),
            }))
        );
    }

    onChange(checked, item) {
        item.enabled = checked;
    }

    apply() {
        const disabledItems = this.items
            .filter((item) => !item.enabled)
            .map((item) => item.id);
        this.props.onApply(disabledItems);
        this.props.close();
    }
}
