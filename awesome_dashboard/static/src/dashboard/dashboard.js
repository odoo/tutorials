/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { CogMenu } from "@web/search/cog_menu/cog_menu";
import { ItemSelectionDialog } from "./item_selection_dialog/item_selection_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, CogMenu };

    setup() {
        this.items = registry.category("dashboard_item_registry").getAll();
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.user = useService("user");
        this.itemsState = useState({
            disabledIds: this.user.settings.awesome_dashboard_items.split(","),
        });
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openItemSelection() {
        this.dialog.add(ItemSelectionDialog, {
            items: this.items,
            disabledIds: this.itemsState.disabledIds,
            onSelectionChanged: this.onSelectionChanged.bind(this),
        });
    }

    onSelectionChanged(newDisabledItems) {
        this.itemsState.disabledIds = newDisabledItems;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
