import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

import { DashboardItem } from "./dashboard_item";
import { ConfigDialog } from "./config_dialog";
import { useLocalStorage } from "./use_local_storage";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { ConfigDialog, DashboardItem, Layout };

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");

        this.statistics = useState(useService("awesome_dashboard.statistics"));

        this.items = registry.category("awesome_dashboard").getAll();
        this.hiddenItems = useLocalStorage("awesome_dashboard.hidden_items", []);

        this.dialogService = useService("dialog");
    }

    openCustomersView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadsView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "kanban"],
                [false, "form"],
            ],
        });
    }

    openConfigDialog() {
        this.dialogService.add(ConfigDialog, {
            hiddenItems: this.hiddenItems,
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
