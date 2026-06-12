import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import "./statistics_service";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template   = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action  = useService("action");
        this.dialog  = useService("dialog");
        this.display = { controlPanel: {} };
        this.stats   = useService("awesome_dashboard.statistics");

        this.state = useState({
            disabledItems: JSON.parse(
                browser.localStorage.getItem("disabledDashboardItems") || "[]"
            )
        });

        this.allItems = registry
            .category("awesome_dashboard.items")
            .getAll();
    }

    get items() {
        return this.allItems.filter(
            item => !this.state.disabledItems.includes(item.id)
        );
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items:         this.allItems,
            disabledItems: this.state.disabledItems,
            onUpdate:      this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
        browser.localStorage.setItem(
            "disabledDashboardItems",
            JSON.stringify(newDisabledItems)
        );
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type:      "ir.actions.act_window",
            name:      "Leads",
            res_model: "crm.lead",
            views:     [[false, "list"], [false, "form"]],
        });
    }
}

class ConfigurationDialog extends Component {
    static template   = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props      = ["close", "items", "disabledItems", "onUpdate"];

    setup() {
        const disabled = Array.isArray(this.props.disabledItems)
            ? this.props.disabledItems
            : [];

        this.items = useState(
            this.props.items.map(item => ({
                ...item,
                enabled: !disabled.includes(item.id),
            }))
        );
    }

    onChange(checked, item) {
        item.enabled = checked;
        const disabled = this.items
            .filter(i => !i.enabled)
            .map(i => i.id);
        this.props.onUpdate(disabled);
    }

    done() {
        this.props.close();
    }
}

registry
    .category("lazy_components")
    .add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
