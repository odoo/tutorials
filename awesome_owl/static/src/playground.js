import { Component, useState } from "@odoo/owl"
import { Counter } from "./components/counter/counter"
import { Card } from "./components/card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
}
