/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";
import { browser } from "@web/core/browser/browser";
import { DashboardDialog } from "./dashboard_dialog/dashboard_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, DashboardDialog };

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.stats_service = useService("awesome_dashboard.statistics");
        this.stats = useState(this.stats_service.load());
        this.items = registry.category("awesome_dashboard_items").get("items");
        this.dialog = useService("dialog");
        this.state = useState({ uncheckedItems: browser.localStorage.getItem("uncheckedItems")?.split(",") || [], });
    }

    openConfiguration() {
        this.dialog.add(DashboardDialog, {
            items: this.items,
            uncheckedItems: this.state.uncheckedItems,
            updateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(uncheckedItems) {
        this.state.uncheckedItems = uncheckedItems;
    }

    showCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "tree"],
                [false, "form"],
            ],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
