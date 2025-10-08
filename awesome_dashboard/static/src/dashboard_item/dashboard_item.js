import { Component } from "@odoo/owl"

export class DashboardItem extends Component {
    static template = "awesome_dashbaord.dashboard_item"

    static props = {
        slot: {
            type: Object,
            shape: {
                default: Object
            }
        },
        size: {
            type: Number,
            default: 1,
            optional: true
        }
    }

}
