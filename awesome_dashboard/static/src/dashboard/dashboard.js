/** @odoo-module **/

import { Component,onWillStart,useState,useRef,onMounted,useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import {Layout} from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import {items} from "./dashboard_items"
import { DashboardItem } from "./DashBoardItem/DashboardItem";
import { PieChart } from "./PieChart/PieChart";

class AwesomeDashboard extends Component {
    setup(){
      
        this.action=useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState(this.statisticsService.stats)
        this.items = items
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
    static components= {Layout,ControlPanel,DashboardItem,PieChart}
    static template = "awesome_dashboard.AwesomeDashboard";
}


registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
// force: true to bypass the studio lazy loading action next time and just use this one directly
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard, { force: true });
