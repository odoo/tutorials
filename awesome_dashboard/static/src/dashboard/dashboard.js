/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { browser } from "@web/core/browser/browser";
import { DashboardConfigDialog } from "./dashboard_config_dialog/dashboard_config_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup(){
        this.action = useService("action");
        this.dialog = useService("dialog");
        const statistics = useService("stats");
        this.stats = useState(statistics.loadStatistics());
        this.items = registry.category("awesome_dashboard").getAll()
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledItems")?.split(",") || []
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
        });
    }

    openConfig(){
        this.dialog.add(DashboardConfigDialog, {
            items: this.items,
            disablesItems: this.state.disabledItems,
            updateConfiguration: this.updateConfiguration.bind(this)
        })
    }

    updateConfiguration(newUpdatedItems){
        this.state.disabledItems = newUpdatedItems
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
