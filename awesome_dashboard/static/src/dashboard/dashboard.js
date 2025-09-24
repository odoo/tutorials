/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardSettingsDialog } from "./settings/settings_dialog";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import "./statistics/statistics_service";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        const stats = this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(stats.statistics);
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.allItems = registry.category("awesome_dashboard").getAll();

        const LS_KEY = "awesome_dashboard.removed_items";
        let removed;
        try { removed = JSON.parse(localStorage.getItem(LS_KEY) || "[]"); } catch { removed = []; }
        this.config = useState({ removed });

        this.loadServerConfig();
        window.awesomeDash = this;
    }

    get items() {
        const removed = new Set(this.config.removed || []);
        return this.allItems.filter(it => !removed.has(it.id));
    }

    openSettings() {
        (this.env?.services?.dialog || this.dialog).add(DashboardSettingsDialog, {
            items: this.allItems,
            removedIds: this.config.removed,
            title: _t("Dashboard items configuration"),
            introLabel: _t("Which cards do you wish to see ?"),
            applyLabel: _t("Apply"),
            onApply: removed => {
                this.config.removed = removed;
                try { localStorage.setItem("awesome_dashboard.removed_items", JSON.stringify(removed)); } catch {}
                this.saveServerConfig(removed);
            },
        });
    }

    async loadServerConfig() {
        try {
            const data = await rpc("/awesome_dashboard/config/get");
            if (Array.isArray(data?.removed)) this.config.removed = data.removed;
        } catch {}
    }

    async saveServerConfig(removed) {
        try { await rpc("/awesome_dashboard/config/set", { removed }); } catch {}
    }

    openOrdersBySize(label) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders: ") + label.toUpperCase(),
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: ["|", "|",
                ["name", "ilike", label],
                ["origin", "ilike", label],
                ["note", "ilike", label]
            ],
        });
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
