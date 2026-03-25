import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "./charts/pie_chart";
import { DashboardItem } from "./dashboard_items/dashboard_item";
import { NumberCard } from "./number_card/number_card";
import { MyDialog } from "./dialog/dialog";
import { browser } from "@web/core/browser/browser";
import { rpc } from "@web/core/network/rpc";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, PieChart, DashboardItem, NumberCard, MyDialog };
    static props = ["*"];

    setup() {
        this.action = useService("action");
        this.statsService = useService("statistics");
        this.statState = useState(this.statsService.state);

        this.dialog = useService("dialog");

        const dashboardRegistry = registry.category("awesome_dashboard").getAll();

        const removedIds = JSON.parse(
            browser.localStorage.getItem("dashboard_removed_items") || "[]",
        );

        this.state = useState({
            items: dashboardRegistry.filter((item) => !removedIds.includes(item.id)),
            allItems: dashboardRegistry,
        });

        onWillStart(async () => {
            const result = await rpc("/awesome_dashboard/user_settings");
            browser.localStorage.setItem(
                "dashboard_removed_items",
                result.removed_ids ? JSON.stringify(result.removed_ids) : "[]",
            );
            if (!result.removed_ids) return;
            this.state.items = dashboardRegistry.filter(
                (item) => !result.removed_ids.includes(item.id),
            );
        });
    }

    openSettings() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.config.settings",
            views: [[false, "form"]],
        });
    }
    viewCustomers() {
        this.action.doAction({
            name: _t("Customers"),
            type: "ir.actions.act_window",
            res_model: "res.partner",
            views: [[false, "kanban"]],
        });
    }
    viewLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            target: "current",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openDialog() {
        this.dialog.add(MyDialog, {
            items: this.state.allItems,
            onApply: () => this.refreshDashboard(),
        });
    }

    async refreshDashboard() {
        const removedIds = JSON.parse(
            browser.localStorage.getItem("dashboard_removed_items") || "[]",
        );
        const result = await rpc("/awesome_dashboard/user_settings/create", {
            removed_ids: removedIds,
        });
        if (result.removed_ids) {
            console.log(result);
            this.state.items = this.state.allItems.filter(
                (item) => !result.removed_ids.includes(item.id),
            );
        } else {
            this.state.items = this.state.allItems.filter((item) => !removedIds.includes(item.id));
        }
    }
}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
