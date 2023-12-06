/** @odoo-module **/

import { Component, useSubEnv } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";


class AwesomeDashboard extends Component {
    setup() {

        // The useSubEnv below can be deleted if you're > 16.0
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });

        this.display = {
            controlPanel: { 
                "top-right": false, 
                "bottom-right": false 
            },
        };
        this.action = useService("action");
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
    openLast7DaysOrders() {
        const domain =
            "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]";
        this.openOrders("Last 7 days orders", domain);
    }

    openLast7DaysCancelledOrders() {
        const domain =
            "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')), ('state','=','cancelled')]";
        this.openOrders("Last 7 days cancelled orders", domain);
    }
}

AwesomeDashboard.components = { Layout };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
