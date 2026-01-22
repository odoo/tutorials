import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item/dashboard_item";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout };

    setup() {
        this.action_service = useService("action");
        this.statistics_service = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            const raw_stats = await this.statistics_service.loadStatistics();
            this.stats = [
                { id: 0, description: "Number of new orders this month", value: raw_stats.nb_new_orders },
                { id: 1, description: "Total amount of new orders this month", value: raw_stats.total_amount },
                { id: 2, description: "Average amount of t-shirt by order this month", value: raw_stats.average_quantity, size: 2 },
                { id: 3, description: "Number of cancelled orders this month", value: raw_stats.nb_cancelled_orders },
                { id: 4, description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'", value: raw_stats.average_time, size: 2 },
            ]
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
