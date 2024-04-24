/* @odoo-module */

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class ConfigurationDialog extends Component {
    static components = { Dialog };
    
    static template = 'awesome_dashboard.ConfigurationDialog';

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
        const saved = localStorage.getItem("unchecked_ids");
        this.unchecked_ids = saved ? JSON.parse(saved) : [];
    }

    onApply() {
        localStorage.setItem("unchecked_ids", JSON.stringify(this.unchecked_ids))
        this.props.onApplied(this.unchecked_ids)
    }

    onChange(ev) {
        const id = ev.srcElement.name
        if (this.unchecked_ids.includes(id)) {
            this.unchecked_ids.splice(this.unchecked_ids.indexOf(id), 1);
        } else {
            this.unchecked_ids.push(id)
        }
        console.log(this.unchecked_ids)
    }
}