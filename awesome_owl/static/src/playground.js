import { Component, markup } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card}
    value1 = markup("<div class='text-danger'>This is the first card content</div>");
}
