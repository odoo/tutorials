/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";

export class ItemsDialog extends Component {
    setup() {
        this.close = this.props.close;

        const currentInvisibleItemIds = JSON.parse(browser.localStorage.getItem("invisibleItemIds")) || [];
        this.itemsSelection = useState(this.props.items.map((item) => {
            return {
                id: item.id,
                description: item.description,
                visible: !currentInvisibleItemIds.includes(item.id)
            };
        }));
    }
    toggleVisibility(item) {
        item.visible = !item.visible;
    }
    apply() {
        browser.localStorage.setItem("invisibleItemIds", JSON.stringify(this.itemsSelection.filter(item => !item.visible)
            .map((item) => item.id)));
        this.props.apply();
        this.close();
    }
}

ItemsDialog.template = "awesome_dashboard.ItemsDialog";
ItemsDialog.components = {
    Dialog,
};
ItemsDialog.props = {
    items: {
        type: Object,
    },
    apply: Function,
    close: Function,
};
