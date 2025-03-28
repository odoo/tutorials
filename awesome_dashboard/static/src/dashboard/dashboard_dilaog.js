import { Component,useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class AwesomeDashboardSettingsDialog extends Component {
  static template = "awesome_dashboard.AwesomeDashboardSettingsDialog";
  static components = { Dialog };
  static props = {
    items: { type: Object },
    hiddenItems: { type: Object },
    onApply: { type: Function }
  };
  setup() {
    this.state = useState({
      hiddenItems: new Set(this.props.hiddenItems),
    });
    // console.log(this.state.hiddenItems);
    
  }

  toggleItem(itemId) {
    if (this.state.hiddenItems.has(itemId)) {
      this.state.hiddenItems.delete(itemId);
    } else {
      this.state.hiddenItems.add(itemId);
    }
  }

  applySettings() {  
    this.props.onApply([...this.state.hiddenItems]); 
  }
}
