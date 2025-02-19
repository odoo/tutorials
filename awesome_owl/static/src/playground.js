/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter,Card}
}
