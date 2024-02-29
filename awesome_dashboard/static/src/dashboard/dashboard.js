/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item/dashboard_item"
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , AwesomeDashboardItem  };

    setup() {
        this.action = useService("action");
        this.display = {
            controlPanel: {},
        };
        this.result_statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialog = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("uncheckedItems")?.split(",") || []
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

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type:"ir.actions.act_window",
            name:"Leads",
            res_model:"crm.lead",
            views:[
                [false,"list"],
                [false,"form"]
            ]
        });
    }

}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };

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

    onChange(checked, item) {
        item.checked = checked;
        const newUncheckedItems = Object.values(this.items)
          .filter((item) => !item.checked)
          .map((item) => item.id);
    
        browser.localStorage.setItem("uncheckedItems", newUncheckedItems);
        this.props.onUpdateConfiguration(newUncheckedItems);
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
