import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class ConfigDialog extends Component {
    static template = "awesome_dashboard.config_dialog";
    static props = {
        items: {type: Array},
        close: {type: Function},
        onApply: {type: Function},
    };
    static components = {Dialog}

    setup() {
        this.state = useState({
            disabledItems: JSON.parse(localStorage.getItem("dashboard_disabled") || "[]")
        });
    }

    apply() {
        localStorage.setItem("dashboard_disabled", JSON.stringify(this.state.disabledItems));
        this.props.onApply(this.state.disabledItems);
        this.props.close();
    }

    toggleItem(id, isChecked) {
        if (isChecked) {
            this.state.disabledItems = this.state.disabledItems.filter(i => i !== id);
        } else {
            this.state.disabledItems = [...this.state.disabledItems, id];
        }
    }
}
