/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { dashboardRegistry } from "../dashboard_registry"; // Import registry

export class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static props = {
        close: { type: Function },  // Accept close function as a prop
    };

    setup() {
        this.dialog = useService("dialog");
    
        // ✅ Get all registered dashboard items
        const allItems = Object.values(dashboardRegistry.getAll());
    
        // ✅ Get currently displayed items from props
        const displayedIds = new Set(this.props.displayedItems.map(item => item.id));
    
        this.state = useState({
            items: allItems.map(item => ({
                id: item.id,
                description: item.description,
                selected: displayedIds.has(item.id), // ✅ Check only displayed items
            })),
        });
    }
    



    applySettings() {
        // Get unchecked items
        const uncheckedItems = this.state.items
            .filter(item => !item.selected)
            .map(item => item.id);

        localStorage.setItem("unchecked_dashboard_items", JSON.stringify(uncheckedItems));

        if (this.props.onSettingsApplied) {
            this.props.onSettingsApplied();
        }



        this.props.close();

        // Later: Store in Odoo settings or trigger a dashboard update
    }
}
