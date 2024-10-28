/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = items;
    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        })
    }

    static components = { Layout, DashboardItem, PieChart };
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
