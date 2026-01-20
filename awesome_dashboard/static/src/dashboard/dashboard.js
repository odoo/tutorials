/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { browser } from "@web/core/browser/browser";
import { DashboardItem } from "./dashboard_item";
import { items } from "./dashboard_items";
import { DashboardConfigurationDialog } from "./dashboard_configuration_dialog"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        const statistics = useService("awesome_dashboard.statistics");
        this.stats = useState(statistics.getStatsResult());
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        let disabled;
        let stored = browser.localStorage.getItem("awesome_dashboard.disabled_items");
        if (stored) {
            disabled = new Set(JSON.parse(stored));
        } else {
            disabled = new Set();
        }
        this.state = useState({ disabled: disabled });
    }

    openConfiguration() {
        this.dialog.add(DashboardConfigurationDialog, {
            disabled: this.state.disabled,
            available: this.items,
            apply: (disabled) => {
                browser.localStorage.setItem(
                    "awesome_dashboard.disabled_items",
                    JSON.stringify(Array(...disabled.values())),
                );
                this.state.disabled = disabled;
            },
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'kanban'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

for (const item of items) {
    registry.category("awesome_dashboard").add(item.id, item);
}
