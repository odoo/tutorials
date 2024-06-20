/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { setHiddenItemIds } from "../dashboard_items";

export class ItemSelectionDialog extends Component {
    static template = "awesome_dashboard.ItemSelectionDialog";
    static components = { Dialog };

    setup() {
        this.items = registry.category("dashboard_item_registry").getAll();
    }

    _confirm() {
        setHiddenItemIds(this.items.filter((item) => !item.show).map((item) => item.id));
        this.props.close();
    }
}
