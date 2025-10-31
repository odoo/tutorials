/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };
    
    static props = {
        items: Array,
        hiddenItems: Array,
        onApply: Function,
        close: Function,
    };

    onApply() {
        const hiddenItemIds = [];
        this.props.items.forEach(item => {
            const checkbox = document.getElementById(item.id);
            if (!checkbox.checked) {
                hiddenItemIds.push(item.id);
            }
        });
        
        this.props.onApply(hiddenItemIds);
        
        this.props.close();
    }
}
