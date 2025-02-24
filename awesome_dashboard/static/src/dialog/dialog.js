/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component,onWillStart } from "@odoo/owl"

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.dashboard"
    static components = { Dialog }

    setup() {
        this.changeVisibility = this.changeVisibility.bind(this)

        onWillStart(() => {
            this.props.items = this.props.items.map((item) => {
                item.isVisible = this.props.inactiveItems.includes(item.id) ? false : true;
                return item
            });
        })
    }

    changeVisibility(id) {
        const item = this.props.items.find((item) => item.id === id)
        if (item) item.isVisible = !item.isVisible
    }

    closeDialog(){
        this.props.close();
        this.props.onChange(this.props.items.filter((item) => !item.isVisible).map((item) => item.id));
    }
}
