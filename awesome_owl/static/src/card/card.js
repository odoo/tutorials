import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = { title: {type: String}, content: {type: String}}

    setup() {
        this.title = this.props.title; 
        this.content = this.props.content;
    }
}