/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { DashboardItem } from "@awesome_dashboard/dashboard/components/dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout ,DashboardItem }

    setup(){
        this.action = useService("action")
        this.dialog = useService("dialog")
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);        
        this.display = { controlPanel: {} }
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        })
    }

    openCustomersKanban(){
        this.action.doAction("base.action_partner_form")
    }

    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views:[
                [false,"list"],
                [false,"form"]
            ]
        })
    }

    openConfigDialog(){
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

}

class ConfigurationDialog extends Component{
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { CheckBox, Dialog };


    setup(){
        this.items = useState(this.props.items.map((item)=>{
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id)
            }
        }))
    }

    done(){
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
