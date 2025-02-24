/** @odoo-module **/

import { Component, useState, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../piechart/piechart";
import { items } from "./dashboard_items";
import { DashboardDialog } from "../dialog/dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardDialog, DashboardItem, Layout, PieChart }
    inactiveItems = useState({items:JSON.parse(localStorage.getItem("inactiveItems") ?? "[]")})

    setup() {
        this.action = useService("action")
        this.dialog = useService("dialog")
        this.data = useState(useService("loadStatistics"));
        this.items = items;
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, 'form'], [false, 'list']]
        })
    }

    onInactiveItemsChange(items){
        this.inactiveItems.items = items;
        localStorage.setItem("inactiveItems", JSON.stringify(this.inactiveItems.items))
    }

    openDashboardDialog() {
        this.dialog.add(DashboardDialog, {
            items: this.items,
            inactiveItems: this.inactiveItems.items,
            onChange: this.onInactiveItemsChange.bind(this)
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
