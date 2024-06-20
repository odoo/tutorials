/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class ItemSelectionDialog extends Component {
    static template = "awesome_dashboard.ItemSelectionDialog";
    static components = { Dialog };
    static props = {
        items: Array,
        close: Function,
        disabledIds: Array,
        onSelectionChanged: Function,
    };

    setup() {
        this.user = useService("user");
        this.itemsWithState = this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledIds.includes(item.id),
            };
        });
    }

    _confirm() {
        const disabledIds = this.itemsWithState.filter((item) => !item.enabled).map((item) => item.id);
        this.user.setUserSettings("awesome_dashboard_items", disabledIds.join(","));
        this.props.onSelectionChanged(disabledIds);
        this.props.close();
    }
}

registry.category("fields").add("test_lgo", ItemSelectionDialog);
