/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };
    
    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            displayItems: browser.localStorage.getItem("displayDashboardItems")?.split(",") || []
        });

    }

    openDialog() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            displayItems: this.state.displayItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    };

    updateConfiguration(newDisplayItems) {
        this.state.displayItems = newDisplayItems;
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLead() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: "crm.lead",
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: Object,
        displayItems: Object,
        onUpdateConfiguration: Function,
        close: Function,
    }

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: this.props.displayItems.includes(item.id),
            }
        }));
    }

    onChange(checked, changedItem){
        changedItem.enabled = checked;
        const newDisplayItems = Object.values(this.items).filter(
            (item) => item.enabled
        ).map((item) => item.id);

        browser.localStorage.setItem("displayDashboardItems", newDisplayItems);

        this.props.onUpdateConfiguration(newDisplayItems);
    }

    apply() {
        this.props.close();
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
