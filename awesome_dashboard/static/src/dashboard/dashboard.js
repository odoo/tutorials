/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { AwesomeDashboardRegistry } from "./dashboard_registry";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";
import { _t, _lt } from "@web/core/l10n/translation";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics_service = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statistics_service.statistics);
        this.items = AwesomeDashboardRegistry.getAll();
        this.dialog = useService("dialog");

        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });

        // Fetch data on mount and set up interval
        onWillStart(() => {
            this.statistics_service.fetchStatistics();
            this.intervalId = setInterval(this.statistics_service.fetchStatistics, 10 * 60 * 1000);
        });

        // Cleanup: Stop fetching when unmounted
        onWillUnmount(() => {
            clearInterval(this.intervalId);
        });
    }

    openCutomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openCrmLead() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("All Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
    }

    openConfigurationDialog() {
        this.dialog.add(ConfigurationDialog, {
            dashboardItems: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
