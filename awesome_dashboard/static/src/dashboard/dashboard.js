import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardDialog } from "./dialog/dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.dashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.display = {
            controlPanel: {}
        };

        this.action = useService("action");
        this.dialog = useService("dialog");

        this.statisticsService = useService("awesome_dashboard.statistics");

        this.statistics = useState(this.statisticsService.statistics);
        this.items = registry.category("awesome_dashboard").getAll();

        this.storageKey = ["awesome_dashboard_item"];
        this.setupActiveDashboardItem();
    };

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",    
            name: "Leads",                    
            res_model: "crm.lead",            
            views: [
                [false, "list"],              
                [false, "form"],              
            ],
            target: "current",                
        });
    }

    openDialog() {
        this.dialog.add(DashboardDialog, {
            items: this.items,
            activeDashboardItem: this.activeDashboardItem,
            storageKey: this.storageKey,
        });
    }

    get activeItems() {
        return this.items.filter(
            (item) => this.activeDashboardItem[item.id]
        );
    }

    setupActiveDashboardItem() {
        const activeDashboardItemList = browser.localStorage.getItem(this.storageKey)?.split(",");

        this.activeDashboardItem = useState({});
        for (const item of this.items) {
            if (activeDashboardItemList) {
                this.activeDashboardItem[item.id] = activeDashboardItemList.includes(
                    item.id.toString()
                );
            } else {
                this.activeDashboardItem[item.id] = true;
            }
        }
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);