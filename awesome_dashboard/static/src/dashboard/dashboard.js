import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigDialog } from "./config_dialog/config_dialog";
import "./statistics_service";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.user = useService("user");

        const { statistics } = useService("awesome_dashboard.statistics");
        this.statistics = useState(statistics);

        this.config = useState({ hiddenIds: [] });
        this.allItems = registry.category("awesome_dashboard").getAll();

        onWillStart(async () => {
            const [user] = await this.orm.read(
                "res.users",
                [this.user.userId],
                ["awesome_dashboard_config"]
            );
            try {
                this.config.hiddenIds = JSON.parse(user.awesome_dashboard_config || "[]");
            } catch {
                this.config.hiddenIds = [];
            }
        });
    }

    get items() {
        return this.allItems.filter((item) => !this.config.hiddenIds.includes(item.id));
    }

    openCustomers() {
        this.action.doAction("contacts.action_contacts");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openConfig() {
        this.dialog.add(ConfigDialog, {
            items: this.allItems,
            hiddenIds: this.config.hiddenIds,
            onApply: async (hiddenIds) => {
                this.config.hiddenIds = hiddenIds;
                await this.orm.write("res.users", [this.user.userId], {
                    awesome_dashboard_config: JSON.stringify(hiddenIds),
                });
            },
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
