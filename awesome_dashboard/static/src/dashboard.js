/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";

import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.action = useService("action");

        this.statistics = useState({})

        onWillStart(async () => {
            this.statistics = await rpc("/awesome_dashboard/statistics");
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'account.move',
            views: [[false, 'list'], [false, 'form']]
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
