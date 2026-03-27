import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };


    setup(){
        this.action = useService("action");
        this.display = useState({
            controlPanel: {}
        });
        this.stats = useState({});
        onWillStart(async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            console.log(result);
            this.stats = result;
            console.log(this.stats.average_quantity);
        })
    }

    
    openCustomers() {
        /* this.action.doAction("base_setup.action_general_configuration"); */

        /* this.action.doAction("base.action_partner_form"); */

        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Customers',
            /* target: 'new', */
            res_model: 'res.partner',
            views: [[false, 'kanban']],
        })
    }
    openLeads() {
        /* this.action.doAction("base.action_partner_form"); */
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            /* res_id: 'crm_lead_action', */
            res_model: 'crm.lead',
            views: [[false, 'list'],[false, 'form']],
        })
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
