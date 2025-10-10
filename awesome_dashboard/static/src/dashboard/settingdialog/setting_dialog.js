/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from '@web/core/utils/hooks';

export class SettingDialog extends Component{
    static template = "awesome_dashboard.SettingDialog";
    static props = {
        close: { type: Function },  // Accept close function as a prop
    };

    setup() {
        this.dialogService = useService("dialog");
        this.state = useState({
            items: this.getItems()
        });
    }

    getItems(){
        // Get uncheckedItemIds from localStorage
        const uncheckedItems = JSON.parse(localStorage.getItem("unchecked_dashboard_items")) || [];
        return Object.values(registry.category("awesome_dashboard").getAll()).map(item => ({
            id: item.id,
            description: item.description,
            enabled: !uncheckedItems.includes(item.id),
        }))
    }

    closeSetting(){
        this.props.close();
    }    

    applySettings() {
        const uncheckedItemIds = this.state.items
            .filter(item => !item.enabled)
            .map(item => item.id);

        // Store uncheckedItemIds in localStorage
        localStorage.setItem("unchecked_dashboard_items", JSON.stringify(uncheckedItemIds));

        this.env.bus.trigger("dashboard_settings_updated");

        this.closeSetting();
    }
}
