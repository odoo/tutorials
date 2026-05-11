import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem};
    setup(){
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");
        this.results = useState(this.statistics.stats);
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
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
    }
    openCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.partner",
            name: _t("Customers"),
            views: [
                [false, "kanban"],
            ],
        });
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            name: _t("Leads"),
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }
    done() {
        this.props.close();
    }
    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)
        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );
        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
