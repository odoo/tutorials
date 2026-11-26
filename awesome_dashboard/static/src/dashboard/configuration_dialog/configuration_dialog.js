import { Component, useProps, signal } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog"
    static components = { Dialog, CheckBox }

    props = useProps(["close", "items", "disabledItems", "onUpdateConfiguration"])

    disabledItems = signal(this.props.disabledItems);

    isEnabled(item) {
        return !this.disabledItems().includes(item.id)
    }

    done() {
        this.props.close()
    }

    onChange(checked, item) {
        const disabled = new Set(this.disabledItems())

        if (checked) {
            disabled.delete(item.id)
        }
        else {
            disabled.add(item.id)
        }
        const newDisabledItems = [...disabled]
        this.disabledItems.set(newDisabledItems)
        this.props.onUpdateConfiguration(newDisabledItems);
    }

}
