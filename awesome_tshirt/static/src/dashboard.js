/** @odoo-module **/

import { Component, useSubEnv, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { getDefaultConfig } from "@web/views/view";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { Card } from './card/card';

class AwesomeDashboard extends Component {
    static defaultFilters = ["('create_date', '>=', (context_today() - datetime.timedelta(days = 7)).strftime('%Y-%m-%d'))"];

    titles = {
        nb_new_orders: 'Number of new orders this month',
        total_amount: 'Total amount of new orders this month',
        average_quantity: 'Average amount of t-shirt by order this month',
        nb_cancelled_orders: 'Number of cancelled orders this month',
        average_time: "Average time for an order to go from 'new' to 'sent' or 'cancelled'"
    };

    keys = ['average_quantity', 'average_time', 'nb_cancelled_orders', 'nb_new_orders', 'total_amount'];
    
    setup() {
        const config = {
            ...getDefaultConfig(),
            ...this.env.config,
        };
        useSubEnv({ config });
        this.action = useService("action");
        this.statisticsService = useService("statisticsService");

        onWillStart(async () => {
            this.statistics = await this.statisticsService.loadStatistics("/awesome_tshirt/statistics");
        });
    }

    openCustomers() {
        this.action.doAction({
            res_model: "res.partner",
            type: "ir.actions.act_window",
            views: [[false, "kanban"]],
            name: this.env._t('Customers'),
        });
    }

    openOrders(name, definedFilters = []) {
        const filters = [...AwesomeDashboard.defaultFilters, ...definedFilters];

        this.action.doAction({
            res_model: "awesome_tshirt.order",
            type: "ir.actions.act_window",
            views: [[false, "list"], [false, "form"]],
            name: this.env._t(name),
            domain: new Domain(`[${filters.join()}]`).toList()
        });
    }


    openNewOrders() {
        this.openOrders('New Orders');
    }

    openCancelledOrders() {
        this.openOrders('Cancelled Orders', ["('state', '=', 'cancelled')"]);
    }

}

AwesomeDashboard.components = { Layout, Card };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
