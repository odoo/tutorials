/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };
    static props = {
        className: { type: String }
    };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")
        });
    }

    customerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    leadAction() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openDialog() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: (newDisabledItems) => {
                this.state.disabledItems = newDisabledItems;
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboardLoader", AwesomeDashboard);
