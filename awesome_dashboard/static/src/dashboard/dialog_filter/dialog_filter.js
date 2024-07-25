/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";



export class DialogFilter extends Component {
    static template = "awesome_dashboard.DialogFilter";
    static components = { Dialog }
    static props = {
        filters: Array,
        onApply: Function,
    };

    onApply() {
        this.props.onApply(this.items);
        this.props.close();
    }

    setup() {
        this.items = useState(this.props.items.values);
    }

    isActive(itemId) {
        return this.items.find(({ id }) => itemId === id).isHidden;
    }

    onCheck(itemId) {
        const item = this.items.find(({ id }) => itemId === id);
        item.isHidden = !item.isHidden
    }
}