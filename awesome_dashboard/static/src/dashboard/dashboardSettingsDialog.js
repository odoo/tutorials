/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static props = {
        items: { type: Object },
        hiddenItems: { type: Object },
        onApply: { type: Function }
      };
    static components = { Dialog };

    setup() {
        this.state = useState({
          hiddenItems: new Set(this.props.hiddenItems),
        });
        console.log(this.state.hiddenItems);
    
      }
    
      toggleItem(itemId) {  
        if (this.state.hiddenItems.has(itemId)) {
            this.state.hiddenItems.delete(itemId);
        } else {
            this.state.hiddenItems.add(itemId);
        }
      }
    
    applyChanges() {
        this.props.onApply([...this.state.hiddenItems]); 
      }
    
    onClose() {
        this.env.services.dialog.close();
    }
    
}
