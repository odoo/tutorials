/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItems } from "./dashboard_items/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItems ,PieChart}

    setup() {
        this.state = useState([])
        const obj = { "total_amount": "Total amount of new orders this month", "nb_new_orders": "Number of new orders this month", "average_quantity": "Average amount of t-shirt by order this month", "nb_cancelled_orders": "Number of cancelled orders this month", "average_time": "Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’" ,"orders_by_size":"Shirts order by Size"}
        this.action = useService('action')
        this.service = useService('loadStatistics')
        onWillStart(async () => {
            const response = await this.service.getData()
            this.state = Object.keys(response)
                .map((key, index) => ({
                    id: index + 1,
                    title: obj[key],
                    name: key,
                    value: response[key],
                    size: index == 1 ? 2 : 1
                }));
        })
    }

    navigateJournal() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

    navigateCustomer() {
        this.action.doAction("base.action_partner_form");
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
