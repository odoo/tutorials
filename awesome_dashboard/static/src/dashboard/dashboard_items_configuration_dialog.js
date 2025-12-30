import { Component, useState, onWillStart } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export const EXCLUDE_FIELDS_KEY="exc_items"

export class DashboardItemsConfigurationDialog extends Component {
    static template = "event.DashboardItemsConfigurationDialog";
    static components = { Dialog }

    static props = {
        close: Function,
        items: Object,
        setExcludeItems: Function
    }

    setup() {
        this.state = useState({ value: JSON.parse(localStorage.getItem(EXCLUDE_FIELDS_KEY)) || [] })
    }

    handleCheckBoxChange(itemId){
        if (this.state.value.includes(itemId)) {
            const itemindex = this.state.value.indexOf(itemId)
            this.state.value.splice(itemindex, 1)
        }else{
            this.state.value.push(itemId)
        }
    }

    handleApply() {
        localStorage.setItem(EXCLUDE_FIELDS_KEY, JSON.stringify(this.state.value))
        this.props.setExcludeItems(this.state.value)
        this.props.close()
    }
}
