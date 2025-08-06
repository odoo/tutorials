/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "./PieChartCard/pie_chart";
import { dashboardCards } from "./dashboard_items";
import { Component, useState } from "@odoo/owl";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.result = useState(this.statistics.stats);
        this.items = useState(dashboardCards);
    }

    get cards() {
        return [
            {
                id: "nb_new_orders",
                description: "New t-shirt orders this month.",
                size: 2,
                props: (data) => ({
                    title: "Number of new orders this month",
                    value: this.result.nb_new_orders,
                }),
            },
            {
                id: "total_amount",
                description: "New orders this month.",
                size: 2,
                title: "Total amount of new order this month",
                value: this.result.total_amount,
            },
            {
                id: "average_quantity",
                description: "Average amount of t-shirt.",
                size: 2,
                title: "Average amount of t-shirt by order this month",
                value: this.result.average_quantity,
            },
            {
                id: "nb_cancelled_orders",
                description: "Cancelled orders this month.",
                size: 2,
                title: "Number of cancelled orders this month",
                value: this.result.nb_cancelled_orders,
            },
            {
                id: "average_time",
                description: "Average time for an order to reach conclusion (sent or cancelled).",
                size: 2,
                title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
                value: this.result.average_time,
            }
        ]
    }

    get chart() {
        return this.result.orders_by_size;
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
    
    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']], // [view_id, view_type]
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.LazyComponent", AwesomeDashboard);
