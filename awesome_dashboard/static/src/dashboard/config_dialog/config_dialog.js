import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";


export class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog, CheckBox }; 
    static props = ["close", "items", "disabledItems", "onUpdateConfigs"];
    setup() {
        
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
        
    }
    
    onChange(checkedItems, Item) {
        Item.enabled = checkedItems;
      
        const updatedDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id);

        this.props.onUpdateConfigs(updatedDisabledItems);
    }

    done() {
        this.props.close();
    }
    
}

