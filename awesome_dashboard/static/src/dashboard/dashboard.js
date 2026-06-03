import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardConfigurationDialog } from "./dashboard_configuration_dialog/dashboard_configuration_dialog";

import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {
        Layout,
        DashboardItem,
        PieChart,
    };

    display = {
        controlPanel: {},
    };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");

        this.statisticsService = useService(
            "awesome_dashboard.statistics"
        );

        this.statistics = useState(
            this.statisticsService.statistics
        );

        const removedItems = JSON.parse(
            localStorage.getItem(
                "awesome_dashboard_removed_items"
            ) || "[]"
        );

        this.items = registry
            .category("awesome_dashboard")
            .getAll()
            .filter(
                item => !removedItems.includes(item.id)
            );
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

    openSettings() {
        this.dialog.add(
            DashboardConfigurationDialog,
            {
                items: registry
                    .category("awesome_dashboard")
                    .getAll(),
            }
        );
    }
}

registry
    .category("lazy_components")
    .add("awesome_dashboard.dashboard", AwesomeDashboard);
