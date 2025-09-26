import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
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

    onDone(){
      const newDisabledItems = this.checkBoxItems.filter(item => !item.enabled).map(item => item.id);
      browser.localStorage.setItem(
          "disabledDashboardItems",
          newDisabledItems,
      );
      this.props.onUpdateConfiguration(newDisabledItems);
      this.props.close();
    }
}
