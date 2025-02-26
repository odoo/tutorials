/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { items } from "./dashboard_items";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup(){
        this.action = useService("action");
        this.statistics = useState(useService("statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    async openLeads(activity){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_id: activity.res_id,
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']]
        });
    }

    openSettings(){
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems){
        this.state.disabledItems = newDisabledItems;
    }

}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.settings_dialog";
    static components = { Dialog, CheckBox };
    static props = ["items", "close", "disabledItems", "onUpdateConfiguration"];

    setup(){
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    onChange(checked, changedItem){
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id);

        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);

        this.props.onUpdateConfiguration(newDisabledItems);
    }

    done(){
        this.props.close();
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
