import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { DashboardConfigDialog } from "./dashboard_config_dialog";
import "./dashboard_items";
import "./statistics_service";

const DASHBOARD_CONFIG_KEY = "awesome_dashboard.config";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        const statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(statisticsService.statistics);
        
        const configStr = localStorage.getItem(DASHBOARD_CONFIG_KEY);
        this.hiddenItems = configStr ? JSON.parse(configStr) : [];
        
        const allItems = registry.category("awesome_dashboard").getAll();
        this.items = allItems.filter(item => !this.hiddenItems.includes(item.id));
    }

    openConfiguration() {
        this.dialog.add(DashboardConfigDialog, {
            currentConfig: this.hiddenItems,
            onApply: (hiddenItems) => {
                this.hiddenItems = hiddenItems;
                localStorage.setItem(DASHBOARD_CONFIG_KEY, JSON.stringify(hiddenItems));
                
                const allItems = registry.category("awesome_dashboard").getAll();
                this.items = allItems.filter(item => !this.hiddenItems.includes(item.id));
            },
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
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
