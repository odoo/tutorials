import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigDialog } from "./config_dialog/config_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem };

    setup() {
        this.actionService = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        this.items = registry.category("awesome_dashboard").get("DashboardItems");
        this.dialog = useService("dialog");
        this.state = useState({
            hiddenIds: browser.localStorage.getItem("dashboard_hidden_ids")?.split(",") || [],
        });
    }

    get displayedItems() {
        return this.items.filter((item) => !this.state.hiddenIds.includes(item.id));
    }

    openConfiguration() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            hiddenIds: this.state.hiddenIds,
            onApply: (newHiddenIds) => {
                this.state.hiddenIds = newHiddenIds;
                browser.localStorage.setItem("dashboard_hidden_ids", newHiddenIds);
            },
        });
    }

    openCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }

    openLeads() {
        this.actionService.doAction({
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
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
