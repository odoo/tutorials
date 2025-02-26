/** @odoo-module **/

import { Component,onWillStart,useState,useRef,onMounted,useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import {Layout} from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashBoardItem/DashboardItem";
import { PieChart } from "./PieChart/PieChart";
import { DashBoardSelection } from "./dashboard_selection";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    setup(){
      
        this.action=useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState({})
        this.items = registry.category("awesome_dashboard.dashboard").getAll();
        this.dialogs = useService("dialog");
        this.dialog_state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });  

         onWillStart(async ()=>{
            console.log("calling service!!")
            this.state=await this.statisticsService.loadStatistics()
            console.log(this.state)
            console.log("JSON HAS BEEN CALLED!!!")
        })
    }
    openDialogView(){
        this.dialogs.add(DashBoardSelection,{items:this.items,disabledItems:this.dialog_state.disabledItems,onUpdateConfiguration:this.updateConfiguration.bind(this)})
    }

    updateConfiguration(newDisabledItems){
        console.log("Configuration updated!!")
        this.dialog_state.disabledItems=newDisabledItems
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

    static components= {Layout,ControlPanel,DashboardItem,PieChart,DashBoardSelection}
    static template = "awesome_dashboard.AwesomeDashboard";
}


registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
// force: true to bypass the studio lazy loading action next time and just use this one directly
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard, { force: true });
