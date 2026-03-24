import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {registry} from "@web/core/registry";
import {getDashboardStorageKey} from "../../dashboard_utility";

export class DashboardConfigurationDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigurationDialog";
    static components = {
        Dialog,
    }
    static props = {
        close: Function,
    }

    setup() {
        super.setup();

        const values = [];

        for (const item of registry.category("awesome_dashboard").getAll()) {
            values.push({id: item.id, description: item.description, visible: localStorage.getItem(getDashboardStorageKey(item.id)) === "true"});
        }

        this.state = useState({
            values,
        });
    }

    onCheckboxChange(value_id, event) {
        this.state.values.find(x => x.id === value_id).visible = event.target.checked;
    }

    async onConfirm() {
        for (const value of this.state.values) {
            localStorage.setItem(getDashboardStorageKey(value.id), value.visible);
        }

        this.props.close();
    }

    onDiscard() {
        this.props.close();
    }
}