/** @odoo-module **/

import { browser } from "@web/core/browser/browser"
import { CheckBox } from "@web/core/checkbox/checkbox"
import { Component, useState } from "@odoo/owl"
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { Dialog } from "@web/core/dialog/dialog"
import { Layout } from "@web/search/layout"
import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"



class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard"

    static components = { Layout, DashboardItem }

    setup() {
        this.display = {controlPanel: {}}
        this.stats = useState(useService("awesome_dashboard.statistics"))
        this.action = useService("action")
        this.items = registry.category("awesome_dashboard").getAll()
        this.dialog = useService("dialog")
        this.state = useState({inactive_cards: browser.localStorage.getItem("disabledDashboardItems")? browser.localStorage.getItem("disabledDashboardItems").split(",") : []})
    }

    viewCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    viewLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'All leads',
            res_model: 'crm.lead',
            views: [[false, 'form'], [false, 'list']],
        })
    }

    updateInactiveCards(new_inactive_cards) {
        this.state.inactive_cards = new_inactive_cards
    }

    openConfigs() {
        this.dialog.add(DashboardConfiguration, {
            items: this.items,
            inactive_cards: this.state.inactive_cards,
            updateInactiveCards: this.updateInactiveCards.bind(this),
        })
    }
}

class DashboardConfiguration extends Component {
    static template = "awesome_dashboard.DashboardConfiguration"

    static components = { CheckBox, Dialog }
    static props = ["close", "items", "inactive_cards", "updateInactiveCards"]

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {...item, enabled: !this.props.inactive_cards.includes(item.id)}
        }))
    }

    apply() {
        const new_inactive_cards = Object.values(this.items).filter((item) => !item.enabled).map((item) => item.id)
        browser.localStorage.setItem("disabledDashboardItems", new_inactive_cards)
        this.props.updateInactiveCards(new_inactive_cards)
        this.props.close()
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard)


