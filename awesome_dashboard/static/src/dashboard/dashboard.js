/** @odoo-module **/

import { Component , useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { PieChart } from "./chart/pie";
import { dashboardRegistry } from "./dashboarditem/dashboard_items";
import { SettingsDialog } from "./dialog/dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem , PieChart};
    setup() {
        this.action = useService("action");
        this.dialogService = useService("dialog");

        this.statisticsService = useService("awesome_dashboard.statistics");      
        this.state = useState(this.statisticsService.state.dashboardItems);

        const savedHiddenItems = JSON.parse(localStorage.getItem("hidden_dashboard_items"));
        this.state.hiddenItems = new Set(savedHiddenItems);

      
    }
    get display() {
        return {controlPanel: {} }
    }
    async openCustomers() {
        
        this.action.doAction("base.action_partner_form");
    }

    async opendialog() {
        this.dialogService.add(SettingsDialog, {
            onApply: (hiddenItems) => {
                this.state.hiddenItems = new Set(hiddenItems);
            },
        });
    }
    async openCrmlead() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name:'crm leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'],[false, 'form']],
        });
    }
    get visibleItems() {
        return Object.values(dashboardRegistry.getAll()).filter(item => !this.state.hiddenItems.has(item.id));
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
