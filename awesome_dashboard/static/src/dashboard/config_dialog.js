import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigDialog extends Component {
    static components = { Dialog, CheckBox };
    static template = "awesome_dashboard.ConfigDialog";

    setup() {
        this.state = useState({
            disabledItems: [...this.props.disabledItems],
        });
    }

    toggleItem(id) {
        if (this.state.disabledItems.includes(id)) {
            this.state.disabledItems = this.state.disabledItems.filter(i => i !== id);
        } else {
            this.state.disabledItems.push(id);
        }
    }

    onApply() {
        this.props.onApply(this.state.disabledItems);
        this.props.close();
    }
}
