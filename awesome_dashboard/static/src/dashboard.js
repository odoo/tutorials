/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { Component, onWillStart, useState } from "@odoo/owl";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.cards = useState([
            {
                id: 1,
                size: 0,
                title: "Number of new orders this month",
                value: 0,
            },
            {
                id: 2,
                size: 0,
                title: "Total amount of new order this month",
                value: 0,
            },
            {
                id: 3,
                size: 0,
                title: "Average amount of t-shirt by order this month",
                value: 0,
            },
            {
                id: 4,
                size: 0,
                title: "Number of cancelled orders this month",
                value: 0,
            },
            {
                id: 5,
                size: 0,
                title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
                value: 0,
            }
        ]);

        onWillStart(async () => {
            this.result = await this.statistics.loadStatistics();
            this.cards = [
                {
                    id: 1,
                    size: 2,
                    title: "Number of new orders this month",
                    value: this.result.nb_new_orders,
                },
                {
                    id: 2,
                    size: 2,
                    title: "Total amount of new order this month",
                    value: this.result.total_amount,
                },
                {
                    id: 3,
                    size: 2,
                    title: "Average amount of t-shirt by order this month",
                    value: this.result.average_quantity,
                },
                {
                    id: 4,
                    size: 2,
                    title: "Number of cancelled orders this month",
                    value: this.result.nb_cancelled_orders,
                },
                {
                    id: 5,
                    size: 2,
                    title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
                    value: this.result.average_time,
                }
            ]
        });
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

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
