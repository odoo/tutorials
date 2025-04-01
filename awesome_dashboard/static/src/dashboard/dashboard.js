/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService,useBus } from "@web/core/utils/hooks";
import { PieChart } from "./piechart.js"; 
import { items } from "../dashboard_items.js";
import { SettingDialog } from "./dialog.js";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, PieChart,SettingDialog ,DashboardItem };

    setup() {
        this.state = useState({items:[]})
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data); 
        this.action = useService("action");
        this.dialogService = useService("dialog");
        // console.log(this.statistics);
        // console.log(this.items);
        const awesomeDashboardRegistry = registry.category("awesome_dashboard");
        this.state.items=Object.values(awesomeDashboardRegistry.getAll())
        this.layoutProps = { controlPanel: {} };

        useBus(this.env.bus, "dashboard_settings_updated", async () => {
            // console.log("dashboard_settings_updated event received");
            await this.getItems();
        });

        this.getItems()
    }
    async getItems(){
        this.state.items = []
        const uncheckedItems = JSON.parse(localStorage.getItem("unchecked_dashboard_items")) || [];
        // console.log(uncheckedItems);
        const dashboardRegistry = registry.category("awesome_dashboard");
        this.state.items = Object.values(dashboardRegistry.getAll())
            .filter(item => !uncheckedItems.includes(item.id));
    }

    openSettings() {
        if (!this.dialogService) {
            console.error("Dialog service is not available.");
            return;
        }
        this.dialogService.add(SettingDialog, { close: () => {} }); 
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
