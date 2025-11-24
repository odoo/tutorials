import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };
    static props = {
        items: Array,
        removedIds: Array,
        onSave: Function,
        close: { type: Function, optional: false },
    };
    setup() {
        const removedIds = this.props.removedIds || []; 
        this.state = useState({
            selected: new Set(this.props.items.map(i => i.id).filter(id => !removedIds.includes(id))),
        });
        this.toggleItem = (id) => {
            if (this.state.selected.has(id)) {
                this.state.selected.delete(id);
            } else {
                this.state.selected.add(id);
            }
        };
    }

    save() {
        const unchecked = this.props.items.map(item => item.id).filter(id => !this.state.selected.has(id));
        this.props.onSave(unchecked);
        this.props.close();
    }
}
