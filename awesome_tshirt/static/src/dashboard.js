/** @odoo-module **/

import { Component, useSubEnv } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { getDefaultConfig } from "@web/views/view";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";


class AwesomeDashboard extends Component {
    static defaultFilters = ["('create_date', '>=', (context_today() - datetime.timedelta(days = 7)).strftime('%Y-%m-%d'))"];
    setup() {
        const config = {
            ...getDefaultConfig(),
            ...this.env.config,
        };
        useSubEnv({ config });
        this.action = useService("action");
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

AwesomeDashboard.components = { Layout };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
