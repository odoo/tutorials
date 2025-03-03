import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { DashboardItem } from "./dashboardItem/dashboarditem";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialog = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();
        const storedDisabledItems = browser.localStorage.getItem("disabledDashboardItems");
        this.state = useState({
            disabledItems: storedDisabledItems ? storedDisabledItems.split(",") : [],
        });
    }

    openCustomersAction() {
        this.actionService.doAction("base.action_partner_form");
    }

    openLeadsAction() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
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
    static template = "awesome_dashboard.configurationdialog";
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

    onChange(event, changedItem) {
        changedItem.enabled = event.target.checked;
        const newDisabledItems = this.items.filter((item) => !item.enabled).map((item) => item.id);
        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems.join(","));
        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
