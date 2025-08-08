/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { MyDialog } from "./dialogue/dialogue";


console.log("🔥 Dashboard module loaded");
export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, MyDialog};
    
    setup() {
        this.items  = useState(registry.category("misc").get("awesome_dashboard.items"));
        if (!localStorage.getItem("unchecked")) {
            console.log("New required!");
            localStorage.setItem("unchecked", JSON.stringify([])); // store as array
        }
        else{
            console.log("already exists!")
        }
        this.updateSet();
       
        this.action = useService("action");
        this.dialog = useService("dialog");
        
       this.result = useState(useService("aleksaStatistics"));
     

       
       console.log(this.result.average_quantity);

    }
    view_customers(){
        this.action.doAction("base.action_partner_form");
    }

    

    openDialog() {
        this.dialog.add(MyDialog, {
            callbackFunc: this.updateSet.bind(this),
            
        });
    }

    updateSet() {
      
        let uncheckedSet = new Set(JSON.parse(localStorage.getItem("unchecked")));
       
        this.items.forEach(item => {
            item.checked = !uncheckedSet.has(item.id);
            
        });
      
       
    }
  

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Lead'),
            target: 'current',
            res_model: 'crm.lead',
            views:[[false, 'list'], [false, 'form']]
        });
    }
   
}

//registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
