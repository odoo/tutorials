import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "Card";
    static props = ["title", "content"];
}
