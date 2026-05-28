import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog };
    static props = {
        items: Array,
        hiddenIds: Array,
        close: Function,
        onApply: Function,
    };

    setup() {
        this.unchecked = useState(new Set(this.props.hiddenIds));
    }

    toggle(id) {
        if (this.unchecked.has(id)) {
            this.unchecked.delete(id);
        } else {
            this.unchecked.add(id);
        }
    }

    apply() {
        this.props.onApply([...this.unchecked]);
        this.props.close();
    }
}
