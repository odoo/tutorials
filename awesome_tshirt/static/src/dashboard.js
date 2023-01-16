/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { Card } from "./card/card";
const { Component, useSubEnv, onWillStart } = owl;
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./pie_chart/pie_chart";
import { loadJS } from "@web/core/assets";
import { sprintf } from "@web/core/utils/strings";
import { Domain } from "@web/core/domain";

class AwesomeDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.tshirtService = useService("tshirtService");

        this.keyToString = {
            average_quantity: this.env._t("Average amount of t-shirt by order this month"),
            average_time: this.env._t(
                "Average time for an order to go from 'new' to 'sent' or 'cancelled'"
            ),
            nb_cancelled_orders: this.env._t("Number of cancelled orders this month"),
            nb_new_orders: this.env._t("Number of new orders this month"),
            total_amount: this.env._t("Total amount of new orders this month"),
        };

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onWillStart(async () => {
            this.statistics = await this.tshirtService.loadStatistics(); // tshirtService is injected in the setup function of the component by the service
        });
        // The useSubEnv below can be deleted if you're > 16.0
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });

        this.display = { // This is the default display
            controlPanel: { "top-right": false, "bottom-right": false },
        };
    }

    openCustomersKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openOrders(title, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "awesome_tshirt.order",
            domain: new Domain(domain).toList(),
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openNewOrders() {
        // Open a list view with all orders created in the last 7 days
        this.action.doAction({
            type: "ir.actions.act_window",
            name: this.env._t('New Orders'),
            res_model: "awesome_tshirt.order",
            views: [[false, "list"]],
            domain: [["create_date", ">", moment().subtract(7, "days").format("YYYY-MM-DD")]],
        });
    }

    openCancelledOrders() {
        // Open a list view with all orders created in the last 7 days
        this.action.doAction({
            type: "ir.actions.act_window",
            name: this.env._t('Cancelled Orders'),
            res_model: "awesome_tshirt.order",
            views: [[false, "list"]],
            domain: [["state", "=", "cancel"]],
        });
    }

    openFilteredBySizeOrders(size) {
        const title = sprintf(this.env._t("Filtered orders by %s size"), size);
        const domain = `[('size','=', '${size}')]`;
        this.openOrders(title, domain);
    }

    openFilteredBySizeOrders(size) {
        const title = sprintf(this.env._t("Filtered orders by %s size"), size);
        const domain = `[('size','=', '${size}')]`;
        this.openOrders(title, domain);
    }
}

AwesomeDashboard.components = { Layout, Card, PieChart };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
