import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout';
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { browser } from "@web/core/browser/browser";
import { DashboardSettingsDialog } from  "./settings_dialog/settings_dialog"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, DashboardSettingsDialog }

    setup() {
        this.action =  useService("action")
        this.dialog = useService("dialog");
        
        this.display = { 
            controlPanel: {
             "layout-buttons": true
            }
        };
        
        const statsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(statsService.statistics);

        this.state = useState({
            items: this.getFilteredItems()
        });
        
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    getFilteredItems() {
        const allItems = registry.category("awesome_dashboard").getAll();
        const removedIds = JSON.parse(browser.localStorage.getItem("awesome_dashboard.removed_ids") || "[]");
        return allItems.filter(item => !removedIds.includes(item.id));
    }

    openConfiguration() {
        this.dialog.add(DashboardSettingsDialog, {
            onConfigSaved: () => {
                this.state.items = this.getFilteredItems();
            }
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);