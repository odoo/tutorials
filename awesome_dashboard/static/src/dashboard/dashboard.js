import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Configuration } from "./configuration/configuration";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup(){
        this.display = {ControlPanel: {}}
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'All leads',
            res_model: 'crm.lead',
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }

    updateItems(disabledItems){
        this.state.disabledItems = disabledItems;
        browser.localStorage.setItem("disabledDashboardItems", disabledItems);
    }

    openConfiguration() {
        this.dialog.add(Configuration, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            update: this.updateItems.bind(this),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
