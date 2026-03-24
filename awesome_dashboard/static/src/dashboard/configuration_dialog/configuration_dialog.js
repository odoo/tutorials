import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };

    static props = {
        close: Function,
        items: { type: Object },
        initialIncludedIds: { type: Array },
        onSave: { type: Function },
    };

    setup() {
        console.log('here');
        console.log(this.props.items);

        console.log(new Set(this.props.items.map((item) => item.id)));

        this.state = useState({
            includedIds: new Set(this.props.initialIncludedIds),
        });
    }

    async _done() {
        const finalIds = Array.from(this.state.includedIds);

        browser.localStorage.setItem("dashboard.includedItemIds", JSON.stringify(finalIds));

        this.props.onSave(finalIds);
        this.props.close();
    }

    onChange(itemId) {
        if (this.state.includedIds.has(itemId)) {
            this.state.includedIds.delete(itemId);
        } 
        else {
            this.state.includedIds.add(itemId);
        }
    }
    
}
