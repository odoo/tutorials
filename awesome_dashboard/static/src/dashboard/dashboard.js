/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboardItem";
import { items } from "./items";
import { ConfigurationDialog } from "./configurationDialog/ConfigurationDialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        const disabledItems = browser.localStorage.getItem("disabledDashboardItems");
        this.items = items;
        this.dialog = useService("dialog");

        if (disabledItems) {
            this.items = this.items.map((el) => {
                return {
                    ...el,
                    disabled: disabledItems.includes(el.id),
                };
            });
        }
        this.items = useState(this.items);
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    async updateStatistics() {
        this.statistics = await this.rpc("/awesome_dashboard/statistics");
        setInterval(async () => {
            this.statistics = await this.rpc("/awesome_dashboard/statistics");
        }, 10000);
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
