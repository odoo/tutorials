import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { ConfigurationDialog } from "./configuration_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("statistics_service"));
        this.dialogService = useService("dialog");
        const savedConfig = browser.localStorage.getItem("dashboard_removed_items");
        this.state = useState({
            removedItems: savedConfig ? JSON.parse(savedConfig) : [],
        });
    }

    get items() {
        return registry
            .category("awesome_dashboard")
            .getAll()
            .filter((item) => !this.state.removedItems.includes(item.id));
    }

    openConfiguration() {
        this.dialogService.add(ConfigurationDialog, {
            initialRemovedItems: this.state.removedItems,
            onApply: (newRemovedIds) => {
                this.state.removedItems = newRemovedIds;
            },
        });
    }

    openCustomers() {
        this.action.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "res.partner",
                name: "Partner Form",
                view_mode: "kanban",
                views: [[false, "kanban"]],
            }
        );
    }

    openLeads() {
        this.action.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "crm.lead",
                name: "Lead Form",
                view_mode: "list,form",
                views: [[false, "list"], [false, "form"]],
            }
        );
    }


}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
