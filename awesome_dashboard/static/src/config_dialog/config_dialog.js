import { Component } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";


export class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog, CheckBox };

    static props = {
        items: { type: Object },
    };

    applyConfig() {
        let hidden_item_ids = this.props.items.filter(item => !item.visible).map(item => item.id);
        browser.localStorage.setItem("hidden_item_ids", hidden_item_ids);
        this.props.close();
    }
}
