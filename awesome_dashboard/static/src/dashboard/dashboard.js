import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { ConfigDialog } from "./config_dialog/config_dialog";
import { Card } from "./cards/card";
import { session } from "@web/session";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, Card, ConfigDialog, CheckBox };

    setup() {
        this.useLocalStorage = false;
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        this.stats = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.stats.loadStatistics());
        this.items = useState({ value: [] });
        this.applyVisibility(this.loadVisibility());
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    saveVisibility(states) {
        if (this.useLocalStorage) {
            browser.localStorage.setItem("awesome_dashboard_visibility", JSON.stringify(states));
        } else {
            this.orm.call(
                "res.users.settings",
                "set_res_users_settings",
                [[session.storeData.Store.settings.id]],
                {
                    new_settings: { "dashboard_layout": JSON.stringify(states) }
                }
            );
        }
        this.applyVisibility(states);
    }

    loadVisibility() {
        let json;
        if (this.useLocalStorage) {
            json = browser.localStorage.getItem("awesome_dashboard_visibility");
        } else {
            json = session.storeData.Store.settings.dashboard_layout;
        }

        if (json) {
            return JSON.parse(json);
        } else {
            // Not defined yet!
            let states = {};
            registry.category("awesome_dashboard").get("items")
                .forEach((item) => states[item.id] = true);
            return states;
        }
    }

    applyVisibility(states) {
        this.items.value = registry.category("awesome_dashboard")
            .get("items")
            .filter((item) => states[item.id]);
    }

    showDialog() {
        const states = this.loadVisibility();
        const dialogItems = registry.category("awesome_dashboard")
            .get("items")
            .map((item) => { return {
                id: item.id,
                enabled: states[item.id],
                label: item.description
            }});
        this.dialogService.add(ConfigDialog, {
            title: _t("Dashboard items configuration"),
            description: _t("Which cards do you wish to see ?"),
            items: dialogItems,
            confirm: this.saveVisibility.bind(this)
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
