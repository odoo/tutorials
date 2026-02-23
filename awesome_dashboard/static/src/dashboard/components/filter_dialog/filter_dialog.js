import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class FilterDialogue extends Component {
    static template = "awesome_dashboard.FilterDialogue";

    static components = { Dialog, CheckBox };

    static props = {
        close: Function,
        items: Object,
        disabledItems: Object, 
        onUpdate: Function,
    };

    setup() {
        const configuration = this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            };
        });
        this.state = useState({ items: configuration });
    }

    toggleItem(id) {
        const item = this.state.items.find(i => i.id === id);
        if (item) {
            item.enabled = !item.enabled;
        }
    }

    applyFilters() {
        const disabledIds = this.state.items
            .filter(item => !item.enabled)
            .map(item => item.id);
        
        browser.localStorage.setItem("disabledDashboardItems", JSON.stringify(disabledIds));

        this.props.onUpdate(disabledIds);
        this.props.close();
    }
}
