/** @odoo-module **/


import { useService } from "@web/core/utils/hooks";
import { getDefaultConfig } from "@web/views/view";
import { Component, useSubEnv } from "@odoo/owl";
import { Domain } from "@web/core/domain";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { onWillStart } from "@odoo/owl";
import { Card } from "./card/card"



class AwesomeDashboard extends Component {
    statistic_key_to_title = {
        "average_quantity": this.env._t("Average amount of t-shirt by order this month"),
        "average_time": this.env._t("Average time for an order to go from 'new' to 'cancelled'"),
        "nb_cancelled_orders": this.env._t("Number of cancelled orders this month"),
        "nb_new_orders": this.env._t("Number of new orders this month"),
        "total_amount": this.env._t("Total amount of new orders this month"),
    }

    setup() {
        const tshirtStatisticsService = useService("tshirtStatisticsService");
        onWillStart(async () => {
            this.statistics = await tshirtStatisticsService.get()
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
