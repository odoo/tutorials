/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item"
import { Layout } from "@web/search/layout";
import { PieChart } from "../pie_chart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {DashboardItem, Layout, PieChart}

    setup(){
        this.action = useService("action");
        this.display = {
            controlPanel : {}
        }
        this.statistics_data = useState(useService("awesome_dashboard.statistics"))
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.dialog_state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomerView(){
        this.action.doAction("base_setup.action_general_configuration")        
    }

    updateConfiguration(newDisabledItems) {
        this.dialog_state.disabledItems = newDisabledItems;
    }

    openCrmLeadView(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false, 'list'],
                [false, 'form'],
            ]
        })
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.dialog_state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }
}

class ConfigurationDialog extends Component{
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }))
    }

    onDone() {
        this.props.close()
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
