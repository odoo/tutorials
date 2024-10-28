/** @odoo-module **/

import {Component, onWillStart, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout"

import "../../statistics"
import {DashboardGrid} from "./dashboard_grid/dashboard_grid"
import {DashboardGridManager} from "./dashboard_objects";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.awesome_dashboard";
    static components = {Layout, DashboardGrid}

    setup() {
        this.action = useService("action")

        onWillStart(this.willStart)

        this.gridManager = useState(new DashboardGridManager())
        this.gridManager.addItem(
            {type: 'stat', title: 'New Orders', stat: 'nb_new_orders'},
            {pos: {x: 0, y: 0}, size: {x: 1, y: 1}}
        )
        this.gridManager.addItem(
            {type: 'stat', title: 'Total Amount', stat: 'total_amount'},
            {pos: {x: 1, y: 0}, size: {x: 2, y: 1}}
        )
        this.gridManager.addItem(
            {type: 'stat', title: 'Average t-shirts/order', stat: 'average_quantity'},
            {pos: {x: 3, y: 0}, size: {x: 1, y: 1}}
        )
        this.gridManager.addItem(
            {type: 'stat', title: 'Canceled Orders', stat: 'nb_cancelled_orders'},
            {pos: {x: 0, y: 1}, size: {x: 1, y: 1}}
        )
        this.gridManager.addItem(
            {type: 'chart', title: 'OrdersBySize', stat: 'orders_by_size'},
            {pos: {x: 1, y: 1}, size: {x: 2, y: 1}}
        )
        this.gridManager.addItem(
            {type: 'stat', title: 'Average Time', stat: 'average_time'},
            {pos: {x: 3, y: 1}, size: {x: 1, y: 1}}
        )
    }

    async willStart() {

    }

    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    async openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
