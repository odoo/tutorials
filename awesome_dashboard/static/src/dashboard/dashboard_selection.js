import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import {Component,useState} from "@odoo/owl";
import { browser } from "@web/core/browser/browser";

export class DashBoardSelection extends Component{
    static components={Dialog,CheckBox}
    static props= ["close","items","disabledItems","onUpdateConfiguration"]
    static template = "awesome_dashboard.dashboard_selection"
    
    setup(){
        this.items = useState(this.props.items.map((item)=>{     
            return{
            ...item,
            enabled: !this.props.disabledItems.includes(item.id) }
        }
       
        ))
    }

    onDone(){
        this.props.close()
    }

    onChange(checked,changedItem){
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item)=>item.id);

        browser.localStorage.setItem("disabledDashboardItems",newDisabledItems);

        this.props.onUpdateConfiguration(newDisabledItems)

    }

}
