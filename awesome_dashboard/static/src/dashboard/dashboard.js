/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItems } from "./dashboard_items/dashboard_item";
import { DashboardDialog } from "./dashboard_dialog/dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItems, DashboardDialog }

    setup() {
        this.state = useState([])
        this.action = useService('action')
        this.service = useService('loadStatistics')

        onWillStart(async () => {
            const response = await this.service.getData()
            this.state = Object.keys(response)
                .map((key) => ({
                    id: key,
                    Component: this.service.itemData.find((o) => o[key])?.component,
                    size: this.service.itemData.find((o) => o[key])?.size || 1,
                    props: {
                        title: this.service.itemData.find((o) => o[key])?.[key] || key,
                        value: response[key],
                    },
                }));
        })

    }

    navigateJournal() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        });
    }

    navigateCustomer() {
        this.action.doAction("base.action_partner_form");
    }

    openDashboardDialog() {
        this.dialog.add(DashboardDialog, {
            items: this.items,
            inactiveItems: this.inactiveItems.items,
            onChange: this.onInactiveItemsChange.bind(this)
        })
    }
}
