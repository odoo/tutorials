import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        content : { type: String, optional: true },
        slots: { type: Object, optional: true },
    };
}
