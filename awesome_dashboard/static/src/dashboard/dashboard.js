import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboard_item";
import { DashboardSettingsDialog } from "./settings_dialog";
import { _t } from "@web/core/l10n/translation";

class AwesomeDashboard extends Component {
    static components = {
        Layout,
        DashboardItem,
        DashboardSettingsDialog,
    };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");
        this.orm = useService("orm");

        this.state = useState({
            stats: this.statistics.state,
            items: [],
        });

        this.labels = {
            customers: _t("Customers"),
            leads: _t("Leads"),
        };
        onWillStart(async () => {
            await this.loadItems();
        });
    }

    async loadItems() {
        const allItems = registry.category("awesome_dashboard.items").getAll();

        const config = await this.orm.call(
            "res.users",
            "get_dashboard_config",
            [],
        );

        const hidden = config?.hidden_items || [];

        this.state.items = allItems.filter(
            (item) => !hidden.includes(String(item.id)),
        );
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Dashboard"),
            target: "new",
            res_model: "crm.lead",
            views: [[false, "list"]],
        });
    }

    openSettings = () => {
        const allItems = registry.category("awesome_dashboard.items").getAll();

        this.dialog.add(DashboardSettingsDialog, {
            title: _t("Settings"),
            items: allItems,
            onApply: async () => {
                await this.loadItems();
            },
        });
    };
}

registry
    .category("lazy_components")
    .add("awesome_dashboard.dashboard", AwesomeDashboard);
