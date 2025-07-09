import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "@awesome_dashboard/dashboard/dashboard-item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

// Main dashboard component
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        // Display configuration for the control panel
        this.display = {
            controlPanel: {},
        };
        
        // Fetching statistics service and storing it in reactive state
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        
        // Accessing action and dialog services
        this.action = useService("action");
        this.dialog = useService("dialog");
        
        // Retrieving dashboard items from the registry
        this.items = registry.category("awesome_dashboard").getAll();
        
        // Managing state of disabled dashboard items
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    // Opens configuration dialog
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    // Navigates to customer form view
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    // Opens leads list and form views
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false,'list'],
                [false,'form'],
            ]
        })
    }

    // Updates configuration of disabled items
    updateConfiguration(newDisabledItems){
        this.state.disabledItems = newDisabledItems;
    }
}

// Configuration dialog component
class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        // Preparing items state with enabled/disabled status
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    // Closes the dialog
    done() {
        this.props.close();
    }

    // Handles checkbox change and updates configuration
    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        // Persisting disabled items in local storage
        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        // Propagating configuration changes
        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

// Registering AwesomeDashboard component in the lazy_components category
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
