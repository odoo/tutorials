/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "./document_item/document_item";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardSettings } from "./dashboard_settings/dashboard_settings";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import {CheckBox} from "@web/core/checkbox/checkbox"
import { browser } from "@web/core/browser/browser";
export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, DashboardSettings};

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.display = {
        controlPanel: {},
        };
        this.dialog = useService("dialog");
        this.allItems = registry.category("awesome_dashboard").getAll();

        this.hiddenItems = JSON.parse(localStorage.getItem("dashboard_hidden") || "[]");

        this.items = this.allItems.filter(
            (item) => !this.hiddenItems.includes(item.id)
        );
        this.state = useState({
        disabledItems:
            browser.localStorage.getItem("disabledDashboardItems")?.split(",") ||
            [],
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
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
