import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class GearMenu extends Component {
    static template = "awesome_dashboard.gearmenu";
    static components = { Dialog };
    static props = {
        close: { type: Function },
        items: { type: Array },
        disabled: { type: Array },
        onUpdate: { type: Function },
    };

    setup() {
        this.state = useState({
            disabledIds: [...this.props.disabled]
        });
    }

    toggleItem(id) {
        if (this.state.disabledIds.includes(id)) {
            this.state.disabledIds = this.state.disabledIds.filter(disabledId => disabledId !== id);
        } else {
            this.state.disabledIds.push(id);
        }
    }

    onApply() {
        this.props.onUpdate(this.state.disabledIds);
        this.props.close(); 
    }
}