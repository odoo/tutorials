import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardSettingsDialog } from "./settings_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.Awesomedashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup(){
        this.action = useService("action");
        this.dialog = useService("dialog"); 
        const statsService = useService("awesome_dashboard.statistics");
        this.statistics = statsService.statistics;
        this.removedItems = useState({
            ids: JSON.parse(localStorage.getItem("awesome_dashboard_removed_items") || "[]"),
        });
        const dashboardRegistry = registry.category("awesome_dashboard");
        this.items = dashboardRegistry.getAll();
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }
    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        })
    }
    openDashboardSettings() {
        this.dialog.add(DashboardSettingsDialog, {
            items: this.items,
            removedItems: this.removedItems.ids,
            onApply: (ids) => {
                this.removedItems.ids = ids;
                localStorage.setItem("awesome_dashboard_removed_items", JSON.stringify(ids));
            },
        });
    }
    get visibleItems() {
        return this.items.filter(
            (item) => !this.removedItems.ids.includes(item.id)
        );
    }

}

registry.category("lazy_components").add("awesome_dashboard.Awesomedashboard", AwesomeDashboard);
