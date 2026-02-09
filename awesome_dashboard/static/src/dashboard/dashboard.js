import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigDialog } from "./config_dialog";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statsService.statistics);
    }

    get items() {
        return registry
            .category("awesome_dashboard")
            .getAll()
            .filter((item) => !this.statistics.disabledItems.includes(item.id));
    }

    openConfiguration() {
        this.dialog.add(ConfigDialog, {
            items: registry.category("awesome_dashboard").getAll(),
            disabledItems: this.statistics.disabledItems,
            onApply: (newDisabledItems) => {
                this.statsService.setDisabledItems(newDisabledItems);
            },
        });
    }

    opencustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openlead() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

registry.category("actions").add("AwesomeDashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
