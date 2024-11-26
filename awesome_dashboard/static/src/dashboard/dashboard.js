/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item";
import { AwesomeDashboardDialog } from "./dashboard_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem, AwesomeDashboardDialog };

    async setup() {
        this.action = useService("action");
        this.data = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.disableItems = useState({items: browser.localStorage.getItem("disabledDashboardItems")});
        this.dialog = useService("dialog");
    }
    openCustomerView() {
        this.action.doAction(
            "base.action_partner_form"
        );
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: 'current',
        });
    }
    openDialog(){
        this.dialog.add(AwesomeDashboardDialog, {
            items: this.items,
            updateDisabledItems: this.updateDisabledItems.bind(this),
        });
        
    }

    updateDisabledItems(disabledItems) {
        this.disableItems.items = disabledItems;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
