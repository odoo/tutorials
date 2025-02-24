/** @odoo-module **/

import { Component,onWillStart,useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import {Layout} from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
class DashboardItem extends Component{
    static template="awesome_dashboard.dashboardItem"
    static defaultProps = {
        size: 1,
      };
    static props=["text","size?"]
}

class AwesomeDashboard extends Component {
    setup(){
        this.action=useService("action");
        this.rpc=rpc
        this.state = useState({})
        this.loadStatistics = memoize(this.loadStatistics.bind(this));
        onWillStart(async ()=>{
            const result = await this.loadStatistics();
            // const result = await this.rpc("/awesome_dashboard/statistics")
            console.log(result)
            this.state = result
        });
       
    }
    async loadStatistics(){
        if (this.state.average_time) {
            console.log("Using cached statistics");
            return this.state;
        }
        console.log("Fetching statistics from the server...");
        // Perform the RPC call if statistics are not cached
        const result = await this.rpc("/awesome_dashboard/statistics");
        
        // Cache the result for later use
        return result;
    }
    openCustomerView(){
        this.action.doAction("base.action_partner_form");
    }
    openLeadView(){
        this.action.doAction({type: 'ir.actions.act_window',
            target: 'current',
            name:["Leads"],
            res_model: 'crm.lead',
            views: [[false, 'form']],})
    }
    static components= {Layout,ControlPanel,DashboardItem}
    static template = "awesome_dashboard.AwesomeDashboard";
}


registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
