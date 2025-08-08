/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class MyDialog extends Component {
    static template = "awesome_dashboard.MyDialog";
    static components = { Dialog };
    static props = {title:{type : String}, callbackFunc:{type:Function}}
    setup() {
      
       
         
        this.items = registry.category("misc").get("awesome_dashboard.items");

        this.uncheckedSet = new Set(JSON.parse(localStorage.getItem("unchecked")));
        
    
        
    }


    updateLocalStorage(){
  
        this.items.forEach(item => {
            let itemState = document.getElementById('input_'+item.id).checked;
            if(!itemState){
                this.uncheckedSet.add(item.id)
            }
            else{
                this.uncheckedSet.delete(item.id);
            }

            
        })
        
        localStorage.setItem("unchecked", JSON.stringify([...this.uncheckedSet]));
        this.props.callbackFunc()
    
    
        

    }
}
