import { Component, xml, useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";

import { DashboardItem } from "./dashboard_item";
import { SettingsDialog } from "./settings_dialog";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = xml`
        <div class="p-2 d-flex gap-2">
            <button t-on-click="gotoCustomers"  class="btn btn-primary">Customers</button>
            <button t-on-click="gotoLeads" class="btn btn-primary">Leads</button>
            <button t-on-click="openSettings" class="btn btn-secondary ms-auto" title="Settings">
                <i class="fa fa-cog"/>
            </button>
        </div>
        <Layout display="{ controlPanel: {} }" className="'o_dashboard h-100'">
            <t t-foreach="items" t-as="item" t-key="item.id">
                <DashboardItem t-if="!item.disabled" size="item.size || 1">
                    <t t-set="itemProp" t-value="item.props ? item.props(statistics) : {'data': statistics}"/>
                    <t t-component="item.Component" t-props="itemProp" />
                </DashboardItem>
            </t>
        </Layout>
    `;

    static components = { Layout, DashboardItem }

    setup() {
        this.action = useService("action")
        this.dialog = useService("dialog")
        this.statistics = useService("awesome_dashboard.statistics")
        const disabled = JSON.parse(browser.localStorage.getItem("disabled_dashboard_items") || "[]")
        this.items = useState(registry.category("awesome_dashboard").getAll().map(
            (item) => ({ ...item, disabled: disabled.includes(item.id) })
        ))
    }

    openSettings() {
        this.dialog.add(SettingsDialog, { items: this.items })
    }

    gotoCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    gotoLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, 'list'], [false, 'form']],
        })
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
