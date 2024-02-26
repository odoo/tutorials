/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox"
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.display = {
            controlPanel: {}
        };
        this.action = useService("action");
        this.dashboardService = useService("dashboard");
        this.result = useState(this.dashboardService);
        this.items = registry.category("items").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openDashboardConfiguration() {
        this.dialog.add(DashboardConfigurationDialog, {
            disabledItems : this.state.disabledItems,
            changeConfiguration: this.changeConfiguration.bind(this)
        });
    }

    changeConfiguration(newDisabledItems){
        this.state.disabledItems = newDisabledItems;
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);



class DashboardConfigurationDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["disabledItems", "close","changeConfiguration"];

    setup() {
        this.items = registry.category("items").getAll();
        this.items.forEach(item => {
            Object.assign(item, {isDisabled: this.props.disabledItems.includes(item.id)})
        });
    }

    closeConfiguration() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.isDisabled = !checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => item.isDisabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.changeConfiguration(newDisabledItems);
    }
}