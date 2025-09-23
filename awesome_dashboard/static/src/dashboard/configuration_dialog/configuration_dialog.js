import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.disabledItems = useState(this.props.disabledItems);
    }

    done() {
        this.props.close();
    }

    onChange(isChecked, changedItemId) {
        this.disabledItems = isChecked
            ? this.disabledItems.filter(i => i !== changedItemId) 
            : [...this.disabledItems, changedItemId];
        this.props.onUpdateConfiguration(this.disabledItems);
    }

}
