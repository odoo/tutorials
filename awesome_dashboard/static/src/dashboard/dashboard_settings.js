import { Component, useState, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.DashboardSettings";

    setup() {
        this.state = useState({
            selected: (this.props.selected || []).map(String),
        });
    }

    toggle(id) {
        const idStr = String(id);
        const selected = this.state.selected.includes(idStr)
            ? this.state.selected.filter((i) => i !== idStr)
            : [...this.state.selected, idStr];
        this.state.selected = selected;
    }

    async save() {
        await this.props.onSave(this.state.selected);
        this.props.close();
    }
}

export class DashboardSettingsDialog extends Component {
    static components = { Dialog, DashboardSettings };
    static template = xml`
        <Dialog title="props.title">
            <DashboardSettings
                items="props.items"
                selected="props.selected"
                onSave="props.onSave"
                close="props.close"
            />
        </Dialog>
    `;
}
