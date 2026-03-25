import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };

    setup() {
        this.state = useState({
            hidden: [...(this.props.hiddenItems || [])],
        });
    }

    apply() {
        this.props.onApply([...this.state.hidden]);
        this.props.close();
    }

    onToggle(ev) {
        const id = ev.target.dataset.id;
        debugger
        if (ev.target.checked) {
            this.state.hidden = this.state.hidden.filter((i) => i !== id);
        } else if (!this.state.hidden.includes(id)) {
            this.state.hidden.push(id);
        }
    }
}

