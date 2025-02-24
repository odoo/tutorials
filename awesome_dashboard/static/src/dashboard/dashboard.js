import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks"
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };  

    setup(){
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        this.dialog = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }  
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    } 
    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form")
    } 
    openLeads(){
        this.action.doAction({
            name: "Leads",
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: [],
        })
    }
}  

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }
    done() {
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
