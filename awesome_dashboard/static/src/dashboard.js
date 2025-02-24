/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Card } from "./card/card";
import { rpc } from "@web/core/network/rpc";
import { loadStatistics } from "./statistics";


class AwesomeDashboard extends Component {
    static components = { Layout, Card };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup(){
        this.action = useService("action");
        this.state = useState({ statistics: [] });
        onWillStart(async () => {
            //this.state.statistics = await rpc("/awesome_dashboard/statistics");
            const stats = await loadStatistics();
            //console.log(stats().then( result => { this.state.statistics = result; } ));
            console.log(stats);
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    async openLeads(activity){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_id: activity.res_id,
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']]
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
