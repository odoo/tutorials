/** @odoo-module **/

const { Component } = owl;

export class DashboardItem extends Component {
    static template = "awesome_owl.dashboardItem";
    static props = {
        slots: { type: Object, optional: true },
        size: { type: Number, optional: true },
        title: String,
        statNumber: Number
    }

    static defaultProps = {
        size: 1
    }
}
