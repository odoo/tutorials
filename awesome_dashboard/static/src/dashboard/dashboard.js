/** @odoo-module **/

import { Component ,useState,onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import {useService} from "@web/core/utils/hooks"
import {DashboardItem} from "./components/dashboardItem/dashboard_item"
import {PieChart} from "./components/pie_chart/pie_chart";
import { DashboardSettingsDialog } from "./setting/dashboard_settings_dialog"
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout,DashboardItem,PieChart };
   
    setup() {
        this.dialog = useService("dialog");
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.items = registry.category("awesome_dashboard.items").getAll();
        this.removedItemIds = useState(this.getRemovedItems());
        this.stats = useState(this.statisticsService.statistics);  // ✅ reactive subscription
    }
    getRemovedItems() {
        return JSON.parse(localStorage.getItem("awesome_dashboard.removed_items") || "[]");
    }
    get visibleItems() {
        return this.items.filter(item => !this.removedItemIds.includes(item.id));
    }
    openSettings() {
        this.dialog.add(DashboardSettingsDialog, {
            items: this.items,
            removedIds: this.removedItemIds,
            onSave: (removed) => {
                localStorage.setItem("awesome_dashboard.removed_items", JSON.stringify(removed));
                this.removedItemIds.splice(0, this.removedItemIds.length, ...removed);
            }
        });
    }
    openCustomer(){
        this.action.doAction("base.action_partner_form")
    }
    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name:"Leads",
            res_model:"crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target:"current"
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
