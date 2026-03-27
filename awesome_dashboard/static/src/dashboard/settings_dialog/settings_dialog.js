import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };

    setup() {
        const saved = this.props.savedRemoved || [];
        this.state = useState({
            removed: [...saved],
        });
    }

    toggle(id) {
        if (this.state.removed.includes(id)) {
            this.state.removed = this.state.removed.filter(i => i !== id);
        } else {
            this.state.removed.push(id);
        }
    }

    apply() {
        this.props.onApply(this.state.removed);
        this.props.close();
    }
}
