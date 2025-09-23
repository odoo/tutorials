/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static styles = ["awesome_dashboard/static/src/dashboard.scss"];
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");

        const savedDisabledItems = user.settings['awesome_dashboard_preferences']
        this.state = useState({ disabledItems: savedDisabledItems ? savedDisabledItems.split(",") : [] });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadsView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"], 
                [false, "form"],
            ],
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
        user.setUserSettings('awesome_dashboard_preferences', newDisabledItems.join(","));
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
