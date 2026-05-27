import { CheckBox } from "@web/core/checkbox/checkbox";
import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { Layout } from "@web/search/layout";
import { Piechart } from "../piechart/piechart";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.awesome_dashboard";
    static components = { Layout, DashboardItem, Piechart };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialog = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();

        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomerList() {
        this.action.doAction("base.action_partner_form");
    }

    openConfig() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfig: this.updateConfig.bind(this),
        })
    }

    openLeadsList() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "CRM Leads Workspace",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    updateConfig(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

class ConfigDialog extends Component {
    static template = "awesome_dashboard.config_dialog";
    static components = { CheckBox, Dialog };
    static props = ["items", "disabledItems", "onUpdateConfig", "close"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    apply() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id);

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.onUpdateConfig(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
