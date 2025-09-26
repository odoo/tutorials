import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";


export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: { type: Array },
        disabledItems: {
            type: Array,
            element: {
                type: { String },
            }
        },
        onUpdateConfig: Function,
        close: Function,
    }

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                id: item.id,
                description: item.description,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    onChange(checked, item) {
        item.enabled = checked;
        const updatedDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id);
        this.props.onUpdateConfig(updatedDisabledItems);
    }

    done() {
        this.props.close();
    }
}
