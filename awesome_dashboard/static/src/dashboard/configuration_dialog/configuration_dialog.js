import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { rpc } from "@web/core/network/rpc";
import { Component, useState } from "@odoo/owl";
    
export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };

    static props = {
        items: Array,
        disabledItems: Array,
        onUpdateConfiguration: Function,
    };

    setup() {
      this.checkBoxItems = useState(this.props.items.map((item) => { // Add 'enabled' field to Item -> return Array of Objects
        return { 
            ...item,
            enabled: !this.props.disabledItems.includes(item.id),
        }
      }));
    }  
    
    onChange(checked, changedItem) {
        changedItem.enabled = checked;
    }

    onDone() {
      const newDisabledItems = this.checkBoxItems.filter(item => !item.enabled).map(item => item.id);
      rpc("/awesome_dashboard/save_settings", { new_disabled_items: newDisabledItems });
      this.props.onUpdateConfiguration(newDisabledItems);
      this.props.close();
    }
}
