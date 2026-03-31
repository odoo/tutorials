import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { onWillStart } from "@odoo/owl";
import { PieChart } from "./pie_chart";
import { useState } from "@odoo/owl";
import { items } from "./dashboard_items";
import { DashboardCard } from "./dashboard_card";
import { DashboardSettingsDialog } from "./dashboard_settings";
import { _t } from "@web/core/l10n/translation";


class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart, DashboardCard };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
            console.log("DASHBOARD SETUP RUNNING ");
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.stats = useState(this.statisticsService.stats);
        this.dialog = useService("dialog");
        this.state = useState({
            hiddenItems: [],
            items: [],
        });

        onWillStart(async () => {
            const hidden = await rpc("/web/dataset/call_kw", {
                model: "res.users",
                method: "get_dashboard_settings",
                args: [[this.env.uid]],
                kwargs: {},
            });
            const allItems = registry.category("awesome_dashboard").getAll();
            const hiddenItems = JSON.parse(hidden || "[]").map(String);
            this.state.hiddenItems = hiddenItems;
            this.state.items = allItems.filter(
                (item) => !hiddenItems.includes(String(item.id))
            );
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    }
    openSettings() {
        const allItems = registry.category("awesome_dashboard").getAll();
        const userId = this.env.uid;
        this.dialog.add(DashboardSettingsDialog, {
            title: _t("Dashboard Settings"),
            items: allItems,
            selected: this.state.hiddenItems, 
            onSave: async (selectedIds) => {
                const normalizedHiddenIds = Array.from(new Set((selectedIds || []).map(String)));
                await rpc("/web/dataset/call_kw", {
                    model: "res.users",
                    method: "set_dashboard_settings",
                    args: [[userId], normalizedHiddenIds],
                    kwargs: {},
                });
                this.state.hiddenItems = normalizedHiddenIds;
                this.state.items = allItems.filter(
                    (item) => !normalizedHiddenIds.includes(String(item.id))
                );
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
