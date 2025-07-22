/** @odoo-module **/

import { Component,useState} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./component/dashboardItem";
import { PieChart } from "./component/pieChart";
import { NumberCard } from "./component/numberCard";
import { DashboardSettingsDialog } from "./component/dashboard_settings_dialog";
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart, NumberCard}

    setup(){
        let staticsService = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");
        this.display = {controlPanel: {} };
        this.action = useService("action");
        this.stats = useState(staticsService.data);
        this.removedItemIds = useState(this.getRemovedItems());
        this.items = registry.category("awesome_dashboard.items").getAll();
    }

    openCustomersKanban()
    {
         this.action.doAction("base.action_partner_form");
    }

    openLeads()
    {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            res_model: "crm.lead",
            views:[
                [false,"list"],
                [false,"form"]
            ]
        });

    }

    get visibleItems() {
        return this.items.filter(item => !this.removedItemIds.includes(item.id));
    }

    getRemovedItems() {
        return JSON.parse(localStorage.getItem("awesome_dashboard.removed_items") || "[]");
    }
    
    openSettings()
    {
         this.dialog.add(DashboardSettingsDialog, {
            items: this.items,
            removedIds: this.removedItemIds,
            onSave: (removed) => {
                localStorage.setItem("awesome_dashboard.removed_items", JSON.stringify(removed));
                this.removedItemIds.splice(0, this.removedItemIds.length, ...removed);
            }
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
