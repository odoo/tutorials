/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboardItem";
import { NumberCard } from "./dashboardItem/number_card";
import { PieChartCard } from "./dashboardItem/pie_chart_card";
import { dashboardRegistry } from "./dashboardItem/dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.dialogService = useService("dialog");
        this.display = {
            controlPanel: {},
            searchPanel: false,
        };
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState(this.statisticsService.state);
    }
    openCustomerForm() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"]],
            context: {
                create: true,
            },
        });
    }

    static components = {
        Layout, DashboardItem, NumberCard, PieChartCard
    };

    get visibleItems() {
        return Object.values(dashboardRegistry.getAll());
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
