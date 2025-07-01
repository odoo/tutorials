import { Component } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.dialog";
    static components = { CheckBox, Dialog };
    static props = [ "title", "items", "storageKey", "activeDashboardItem" ];

    setup() {
        this.items = this.props.items;
        this.storageKey = this.props.storageKey;
        this.activeDashboardItem = this.props.activeDashboardItem;
    }

    toggleActiveItem(itemId) {
        this.activeDashboardItem[itemId] = !this.activeDashboardItem[itemId];
        browser.localStorage.setItem(
            this.storageKey.join(","),
            Object.keys(this.activeDashboardItem).filter(
                (itemId) => this.activeDashboardItem[itemId]
            )
        );
    }
}