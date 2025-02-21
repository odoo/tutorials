/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState, onWillStart } from "@odoo/owl"

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.dashboard"
    static components = { Dialog }

    setup() {
        this.items = useState([])
        this.changeVisibility = this.changeVisibility.bind(this)

        onWillStart(() => {
            this.props.inactiveItems = JSON.parse(localStorage.getItem("inactiveItems") ?? "[]")
            this.items = this.props.items.map((item) => {
                item.isVisible = this.props.inactiveItems.includes(item.id) ? false : true;
                return item
            });
        })
    }

    changeVisibility(id) {
        const item = this.items.find((item) => item.id === id)
        if (item) item.isVisible = !item.isVisible

        localStorage.setItem("inactiveItems", JSON.stringify(this.items.filter((item) => !item.isVisible).map((item) => item.id)))
    }
}
