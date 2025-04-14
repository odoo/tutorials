/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService, useBus } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboarditem/dashboarditem";
import { PieChart } from "./components/piechart/piechart";
import { SettingDialog } from "./components/dialogbox/dialogbox";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout,  PieChart, DashboardItem, SettingDialog}
    setup() {
        this.actionService = useService("action");
        this.dialogService = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);
        this.stats = useState(this.statisticsService.data);
        const dashboardRegistry=registry.category("awesome_dashboard")
        this.state = useState({ items: [] });
        this.items=Object.values(dashboardRegistry.getAll());

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

    openCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }
    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "current",
            views: [[false, 'list'], [false, 'form']],
        });
    }
    openSettings() {
        this.dialogService.add(SettingDialog);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
