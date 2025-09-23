import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    // Explicit Props
    static props = {
        title: String,
        content: String,
    };
}
