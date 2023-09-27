/** @odoo-module **/


import { useService } from "@web/core/utils/hooks";
import { getDefaultConfig } from "@web/views/view";
import { Component, useSubEnv } from "@odoo/owl";
import { Domain } from "@web/core/domain";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { onWillStart } from "@odoo/owl";
import { Card } from "./card/card"

const STATISTIC_TO_CARD_NAME = {
    "average_quantity": "Average amount of t-shirt by order this month",
    "average_time": "Average time for an order to go from 'new' to 'cancelled'",
    "nb_cancelled_orders": "Number of cancelled orders this month",
    "nb_new_orders": "Number of new orders this month",
    "total_amount": "Total amount of new orders this month",
}

class AwesomeDashboard extends Component {


    setup() {
        const tshirtStatisticsService = useService("tshirtStatisticsService");
        onWillStart(async () => {
            const statistics = await tshirtStatisticsService.get()
            this.cards = Object.entries(statistics).map(([name, value], idx) => ({
                idx,
                title: STATISTIC_TO_CARD_NAME[name],
                description: value
            }))
        });

        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });

        this.action = useService("action");
    }

    #openOrders(name, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: name,
            res_model: "awesome_tshirt.order",
            views: [
                [false, "list"],
            ],
            domain: new Domain(domain).toList(),
        });
    }


    openLast7DaysOrders() {
        const domain =
            "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]";
        this.#openOrders(this.env._t("Last 7 days orders"), domain);
    }

    openLast7DaysCancelledOrders() {
        const domain =
            "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')), ('state','=', 'cancelled')]";
        this.#openOrders(this.env._t("Last 7 days cancelled orders"), domain);
    }

    openCustomerView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            res_model: "res.partner",
            views: [
                [false, "kanban"],
            ],
        });
    }
}

AwesomeDashboard.components = { Layout, Card };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
