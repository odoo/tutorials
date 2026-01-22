import { Component, onWillRender, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.action_service = useService("action");
        this.raw_stats = useState(useService("awesome_dashboard.statistics"));
        this.stats = [];

        // Before rendering the dashboard items we want to ensure the values are up to date with the latest update from the statistics service.
        // This would be unnecessary if I pulled values directly from the stateful component 'raw_stats' in dashboard.xml, I'm just messing around 
        // with the hooks to use a data structure defined outside of the statistics service which manages this component's state.
        onWillRender(() => {
            this.stats = [
                { id: 0, description: "Number of new orders this month", value: this.raw_stats.nb_new_orders },
                { id: 1, description: "Total amount of new orders this month", value: this.raw_stats.total_amount },
                { id: 2, description: "Average amount of t-shirt by order this month", value: this.raw_stats.average_quantity, size: 2 },
                { id: 3, description: "Number of cancelled orders this month", value: this.raw_stats.nb_cancelled_orders },
                { id: 4, description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'", value: this.raw_stats.average_time, size: 2 },
            ];
        })
    }

    openPartnerKanbanView() {
        this.action_service.doAction("base.action_partner_form");
    }

    openCrmLeads() {
        this.action_service.doAction({
            type: 'ir.actions.act_window',
            name: 'CRM leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
