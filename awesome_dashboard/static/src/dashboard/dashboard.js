import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "./dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pie_chart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static components = { AwesomeDashboardItem, PieChart, Layout };
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");

        const hiddenItems = JSON.parse(
            browser.localStorage
                .getItem("disabled_dashboard_items")
                ?.split(",") || '[]',
        );
        this.state = useState({ disabledItems: hiddenItems });

        onWillStart(async () => {
            const res = await rpc("/awesome_dashboard/statistics");
            console.log(res);
            Object.assign(this.stats, res);
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "form"],
                [false, "list"],
            ],
        });
    }

    openConfig() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            disabled: this.state.disabledItems,
            onUpdate: (newDisabledItems) => {
                this.state.disabledItems = newDisabledItems;
                browser.localStorage.setItem(
                    "disabled_dashboard_items",
                    JSON.stringify(newDisabledItems),
                );
            },
        });
    }
}

class ConfigDialog extends Component {
    static template = "awesome_dashboard.config";
    static components = { CheckBox, Dialog };

    static props = {
        items: Array,
        close: Function,
        disabled: Array,
        onUpdate: Function,
    };

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                isEnabled: !this.props.disabled.includes(item.id),
            })),
        );
    }

    apply() {
        const disabledIds = this.items
            .filter((i) => !i.isEnabled)
            .map((i) => i.id);

        this.props.onUpdate(disabledIds);
        this.props.close();
    }

    onCheck(item, value) {
        console.log(item, value)
        item.isEnabled = value;
        const updatedDisabledItemsList = Object.values(this.items)
            .filter((item) => !item.isEnabled)
            .map((item) => item.id);

        browser.localStorage.setItem(
            "disabled_dashboard_items",
            updatedDisabledItemsList,
        );

        this.props.onUpdate(updatedDisabledItemsList);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
