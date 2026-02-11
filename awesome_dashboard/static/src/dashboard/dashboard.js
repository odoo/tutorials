/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { Component, onMounted, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { DashboardItem } from "./dashboardItem/dashboardItem";
import { Dialog } from "@web/core/dialog/dialog";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        // services
        this.actionService = useService("action");
        this.dialogService = useService("dialog");
        this.statistics = useState(useService("awesome_dashboard.statistics"));

        // local sotarage data -- will store in user web browser disk
        const savedDisabled =
            browser.localStorage
                .getItem("disabledDashboardItems")
                ?.split(",") || [];

        this.state = useState({
            disabledItems: savedDisabled,
            loading: true,
        });

        // dashboard items from registry
        this.items = registry.category("awesome_dashboard").getAll();

        onMounted(async () => {
            await new Promise((res) => setTimeout(res, 500));
            this.state.loading = false;
        });
    }

    openCustomer() {
        this.actionService.doAction("base.action_partner_form");
    }

    openLeads() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    openConfiguration() {
        this.dialogService.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }))
        );
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;

        const newDisabledItems = this.items
            .filter((item) => !item.enabled)
            .map((item) => item.id);

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry
    .category("lazy_components")
    .add("AwesomeDashboard", AwesomeDashboard);
