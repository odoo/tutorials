import { Component } from '@odoo/owl'

export class NumberCard extends Component {
    static template = "awesome_dashboard.numberCard"
    static components = {}
    static props = {
        title: {
            type: String
        },
        value: {
            type: Number | String
        }
    }
}
