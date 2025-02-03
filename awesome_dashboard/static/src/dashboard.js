/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";



class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem};

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action= useService("action")
        this.state= useState({
            rpcResponse: {}
        })

        onWillStart(async ()=>{
            const result = await rpc('/awesome_dashboard/statistics') //rpc(route, params, settings)
            this.state.rpcResponse = result
        })
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
