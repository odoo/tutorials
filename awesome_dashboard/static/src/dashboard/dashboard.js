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
        this.dialog.add(ItemSelectionDialog);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
