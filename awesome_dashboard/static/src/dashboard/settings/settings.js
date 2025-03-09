import { Component, useState } from "@odoo/owl"
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { CheckBox } from "@web/core/checkbox/checkbox"
import { useService } from "@web/core/utils/hooks"

export class Settings extends Component{
    static template = "awesome_dashboard.settings"
    static components = { Dialog, CheckBox }

    setup(){
        this.items = registry.category("awesome_dashboard").getAll()
        this.dialog = useService("dialog")
        const storedHiddenItems = JSON.parse(localStorage.getItem('hiddenDashboardItems')) || []
        this.state = useState({hiddenItems: new Set(storedHiddenItems)})
    }
    onValueChange = (itemId)=>{
        if(this.state.hiddenItems.has(itemId)){
            this.state.hiddenItems.delete(itemId)
        }
        else{
            this.state.hiddenItems.add(itemId)
        }
    }

    btnDone(){
        localStorage.setItem('hiddenDashboardItems',JSON.stringify([...this.state.hiddenItems]))
        // changes will apply to dashboard
        this.props.onDone([...this.state.hiddenItems])
        this.dialog.closeAll()
    }
}
