import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static template = "awesome_owl.Card"

    static props = {
        content: { type: String, optional: true },
        title: { type: String, optional: true },
    }

}
