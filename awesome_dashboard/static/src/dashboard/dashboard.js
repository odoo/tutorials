import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { dashboardItemsRegistry } from "./dashboard_items";
import { SettingsDialog } from "./dialog/setting_dialog";
import { user } from "@web/core/user";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.state);
        this.allItems = dashboardItemsRegistry.getAll();
        this.state = useState({ hidden: [] });

        onWillStart(async () => {
            await this.statisticsService.initialLoad;
            const [result] = await this.orm.read(
                "res.users", [user.userId], ["dashboard_settings"]
            );
            this.state.hidden = result?.dashboard_settings?.hidden || [];
        });
    }

    get visibleItems() {
        return this.allItems.filter((item) => !this.state.hidden.includes(item.id));
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form");
        console.log(this);
        
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            target: "current",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openSettings() {
        this.dialog.add(SettingsDialog, {
            items: this.allItems,
            hiddenItems: this.state.hidden,
            onApply: async (hiddenIds) => {
                this.state.hidden = hiddenIds;
                await this.orm.write("res.users", [user.userId], {
                    dashboard_settings: { hidden: hiddenIds },
                });
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
