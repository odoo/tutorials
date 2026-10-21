import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.display = { controlPanel: {} };
        const storedDisabledItems = user.settings.awesome_dashboard_disabled_items;
        this.state = useState({
            disabledItems: storedDisabledItems ? storedDisabledItems.split(",").filter(Boolean) : [],
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("All leads"),
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
        });
    }

    async updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
        await user.setUserSettings("awesome_dashboard_disabled_items", newDisabledItems.join(","));
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.title = _t("Dashboard items configuration");
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
        const newDisabledItems = Object.values(this.items)
            .filter((item) => !item.enabled)
            .map((item) => item.id);

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
