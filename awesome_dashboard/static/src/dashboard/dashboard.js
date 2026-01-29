import { Component, useState } from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard };

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.dialog = useService("dialog");
        this.hiddenItemIds = useState(
            browser.localStorage.getItem("hiddenDashboardItemIds")?.split(",") || [],
        );
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openConfig() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            hiddenItemIds: this.hiddenItemIds,
            onUpdateConfig: this.updateConfig.bind(this),
        });
    }

    updateConfig(newHiddenItemIds) {
        this.hiddenItemIds = newHiddenItemIds;
    }
}

class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog, CheckBox };
    static props = {
        close: Function,
        items: { type: Array, elements: Object },
        hiddenItemIds: { type: Array, elements: String },
        onUpdateConfig: { type: Function, optional: true },
    };

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                displayed: !this.props.hiddenItemIds.includes(item.id),
            })),
        );
    }

    onChange(checked, itemToChange) {
        itemToChange.displayed = checked;
        const newHiddenItemIds = this.items
            .filter((item) => !item.displayed)
            .map((item) => item.id);

        browser.localStorage.setItem("hiddenDashboardItemIds", newHiddenItemIds);
        this.props.onUpdateConfig?.(newHiddenItemIds);
    }

    done() {
        this.props.close();
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
