/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"
import { useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, browser}

    setup(){
        this.action = useService("action")
        this.dialog = useService("dialog")
        this.statistics= useState(useService("statisticsService"))
        this.items = registry.category("awesome_dashboard").getAll()
        this.state = useState({excludedItemsIds: this.retrieveExcludedItemsIds()})
    }

    retrieveExcludedItemsIds(){
        return (browser.localStorage.getItem("excludedItemsIds")?.split(",") || [])
    }

    openCustomersKanbanView(){
        this.action.doAction('base.action_partner_form')
    }
    
    openCrmLeadsView(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'CRM Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }
    
    openConfigurationDialog(){
        this.dialog.add(ConfigurationDialog,
        {
            items: this.items,
            excludedItemsIds: this.state.excludedItemsIds,
            updateConfiguration: this.updateConfiguration.bind(this)
        })
    }

    updateConfiguration(excludedItemsIds){
        this.state.excludedItemsIds = excludedItemsIds
        browser.localStorage.setItem("excludedItemsIds", this.state.excludedItemsIds)
    }

}

class ConfigurationDialog extends Component{
    static template = "awesome_dashboard.ConfigurationDialog"
    static components = { Dialog, CheckBox}
    static props = ["close", "items", "excludedItemsIds", "updateConfiguration"]
    
    setup(){
        this.items = this.props.items.map((item) =>{
            return {
                ...item,
                enabled: !this.props.excludedItemsIds.includes(item.id)
            }
        })
    }

    onChange(ev, changedItem){
        changedItem.enabled = ev 
        this.excludedItemsIds = Object.values(this.items).filter(item => !item.enabled).map(item => item.id)
    }

    closeAndUpdateConfiguration(){
        this.props.close()
        this.props.updateConfiguration(this.excludedItemsIds)
    }
    

    
}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
