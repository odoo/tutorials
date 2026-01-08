/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";
import { DashboardSettingsDialog } from "./dashboardSettingsDialog";
import { _t } from "@web/core/l10n/translation";



class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {

        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");

        this.state = useState({
            res: this.statisticsService.data,
            items: registry.category("awesome_dashboard").getEntries(),
            hiddenItems: new Set(JSON.parse(localStorage.getItem("hidden_dashboard_items")) || [],),
        });
        console.log("HhHidden", this.state.hiddenItems);

        onWillStart(async () => {
            try {
                const result = this.state.res;
                this.state.statistics = result;

                console.log("Hidden", this.state.hiddenItems)

            } catch (error) {
                console.error("Error fetching  statistics:", error);
            }
        });
    }

    _t(...args) {
        return _t(...args);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    openSettings() {
        this.env.services.dialog.add(DashboardSettingsDialog, {
            items: this.state.items,
            hiddenItems: [...this.state.hiddenItems], // Convert Set to array
            onApply: (updatedHiddenItems) => {
                if (!this.state.hiddenItems) {
                    this.state.hiddenItems = new Set();
                }

                this.state.hiddenItems = new Set(updatedHiddenItems);
                localStorage.setItem("hidden_dashboard_items", JSON.stringify([...this.state.hiddenItems]));
                this.env.services.dialog.closeAll();

            },
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
