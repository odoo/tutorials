/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardConfigDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigDialog";
    static components = { Dialog };
    static props = ["title", "items", "disabledItems", "close"];

    setup() {
        const savedConfig = JSON.parse(localStorage.getItem("dashboard_config")) || [];
        this.state = useState({
            disabledItems: new Set(savedConfig.length ? savedConfig : this.props.disabledItems || []),
        });
    }

    toggleItem = (itemId) => {
        this.state.disabledItems = new Set(this.state.disabledItems);
        if (this.state.disabledItems.has(itemId)) {
            this.state.disabledItems.delete(itemId);
        } else {
            this.state.disabledItems.add(itemId);
        }
    };

    saveConfig() {
        const disabledItemsArray = [...this.state.disabledItems];
        localStorage.setItem("dashboard_hidden_items", JSON.stringify(disabledItemsArray));

        if (this.props.onSave) {
            this.props.onSave(disabledItemsArray);
        }

        this.props.close();
    }
}