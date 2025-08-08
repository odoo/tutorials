/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup(){
        this.action = useService("action");
        this.statistics = {
            average_quantity: 0,
            average_time: 0,
            nb_cancelled_orders: 0,
            nb_new_orders: 0,
            orders_by_size: {
                m: 0,
                s: 0,
                xl: 0,
            },
            total_amount: 0,
        };
        
        onWillStart(async() => {
            const result = await rpc("/awesome_dashboard/statistics");
            console.log(result);
            this.statistics = result
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            name: "Leads",
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            view_mode: "list,form",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
