import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

/**
 * Main dashboard component that displays configurable widgets
 */
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.actionService = useService("action");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));
        this.dialogService = useService("dialog");
        
        // Control panel configuration
        this.displayOptions = {
            controlPanel: {},
        };
        
        // Get all registered dashboard items
        this.dashboardItems = registry.category("awesome_dashboard").getAll();
        
        // User preferences for dashboard configuration
        this.state = useState({
            disabledItems: this._loadDisabledItems(),
        });
    }

    /**
     * Load disabled dashboard items from localStorage
     * @returns {Array} Array of disabled item IDs
     * @private
     */
    _loadDisabledItems() {
        const savedItems = browser.localStorage.getItem("disabledDashboardItems");
        return savedItems ? savedItems.split(",") : [];
    }

    /**
     * Open dashboard configuration dialog
     */
    openConfiguration() {
        this.dialogService.add(DashboardConfigDialog, {
            items: this.dashboardItems,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    /**
     * Update disabled items when configuration changes
     * @param {Array} newDisabledItems - Updated list of disabled item IDs
     */
    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    /**
     * Navigate to customers view
     */
    openCustomerView() {
        this.actionService.doAction("base.action_partner_form");
    }

    /**
     * Navigate to leads view
     */
    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

/**
 * Dialog component for dashboard configuration
 */
class DashboardConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.configItems = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            };
        }));
    }

    /**
     * Close the dialog
     */
    done() {
        this.props.close();
    }

    /**
     * Handle checkbox change events
     * @param {boolean} checked - New checkbox state
     * @param {Object} changedItem - Item being toggled
     */
    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        
        // Create array of disabled item IDs
        const newDisabledItems = Object.values(this.configItems)
            .filter(item => !item.enabled)
            .map(item => item.id);

        // Save to localStorage
        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        // Update parent component
        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
