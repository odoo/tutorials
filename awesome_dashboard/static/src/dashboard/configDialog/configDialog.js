import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog };
    static props = {
        items: Object,
        onApply: Function,
    };

    setup(){
        this.checkedState = useState({});
        for (const item of this.props.items) {
            this.checkedState[item.id] = !this.props.hiddenIds.includes(item.id);
        }
    }

    toggleItem(itemId){
        this.checkedState[itemId] = !(this.checkedState[itemId]);
    }

    done(){
        const unchecked = Object.entries(this.checkedState)
            .filter(([, value]) => value === false)
            .map(([key]) => key);        

        localStorage.setItem("hidden_dashboard_items", JSON.stringify(unchecked));
        
        this.props.onApply(unchecked);
        this.props.close();
    }

}
