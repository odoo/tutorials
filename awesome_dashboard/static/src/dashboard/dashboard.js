/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "../piechart/piechart";
import { DashboardDialog } from "./dashboard_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, DashboardDialog };

    setup() {
        this.items = registry.category("awesome_dashboard").get("awesome_dashboard_items");
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useState(useService("statistics"));
        this.inactive_items = useState({
            items: browser.localStorage.getItem("inactive_items")?.split(",") || []
        });
    }

    openCustomersKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadsView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'CRM Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openDialog() {
        this.dialog.add(DashboardDialog, {
            items: this.items,
            inactive_items: this.inactive_items.items,
            updateInactiveItems: this.setInactiveItems.bind(this)
        });
    }

    setInactiveItems(inactive_items) {
        browser.localStorage.setItem(
            "inactive_items",
            inactive_items,
        );
        this.inactive_items.items = inactive_items;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
