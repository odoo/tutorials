/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item"
import { browser } from "@web/core/browser/browser";
import { AwesomeDashboardDialog } from "./dashboard_dialog"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem }
    setup(){
        this.action = useService("action");
        /** Previous implementation: leaving here for tutorial review purposes **/
        /** this.statistics = useService("awesome_dashboard.statistics");
        this.data = useState({ });
        onWillStart(async () => {
            this.data = await this.statistics();
        }); **/
        this.data = useState(useService("awesome_dashboard.statistics"));
        this.dashboardItems = registry.category("awesome_dashboard").getAll();
        this.dialogService = useService("dialog");
        if(browser.localStorage.getItem("AwesomeDashboardUncheckedItems") == null){
            browser.localStorage.setItem("AwesomeDashboardUncheckedItems", ({}));
        }
        this.uncheckedItems = useState({dashboardItems: browser.localStorage.getItem("AwesomeDashboardUncheckedItems")});
    }
    openCustomerView(){
        this.action.doAction("base.action_partner_form");
    }
    openLeadsViews() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: 'current',
        });
    }
    openOptionsDialog(){
        this.dialogService.add(AwesomeDashboardDialog, {
            dashboardItems: this.dashboardItems,
            updateUncheckedItems: this.updateUncheckedItems.bind(this),
        });
    }
    updateUncheckedItems(uncheckedItems){
        this.uncheckedItems.dashboardItems = uncheckedItems;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
