/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { browser } from "@web/core/browser/browser";
import { ConfigDialog } from "./config_dialog/config_dialog"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        const { statistics, startAutoRefresh, stopAutoRefresh } = useService("awesome_dashboard.statistics");
        this.result = useState(statistics);
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");

        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledItems")?.split(",") || []
        });

        onWillStart(() => {
            startAutoRefresh();
        });

        onWillUnmount(() => {
            stopAutoRefresh();
        });
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form");
    }
    
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "all leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]]
        });
    }

    openConfig() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfig.bind(this),
        })
    }
    
    updateConfig(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
