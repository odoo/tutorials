import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../piechart/piechart";
import { getDashboardItems } from "../dashboard_items_service";
import { DashboardConfigurationDialog } from "../dashboard_configuration_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        const statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(statisticsService.state);
        const storedConfig = localStorage.getItem("dashboard_configuration");
        this.hiddenItems = storedConfig ? JSON.parse(storedConfig) : [];
        const allItems = getDashboardItems();
        this.items = allItems.filter((item) => !this.hiddenItems.includes(item.id));
    }

    openCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            res_model: "res.partner",
            views: [
                [false, "kanban"],
                [false, "form"],
                [false, "list"],
            ],
        });
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

    openConfigurationDialog() {
        this.env.services.dialog.add(DashboardConfigurationDialog, {
            onConfigChange: () => {
                const storedConfig = localStorage.getItem("dashboard_configuration");
                this.hiddenItems = storedConfig ? JSON.parse(storedConfig) : [];
                const allItems = getDashboardItems();
                this.items = allItems.filter((item) => !this.hiddenItems.includes(item.id));
                this.render();
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
