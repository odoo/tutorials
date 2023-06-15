/** @odoo-module **/

import { Component,useState } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Todolist } from "./TodoList/todolist";
import { Card } from "../../../awesome_tshirt/static/src/Card/card";
export class Playground extends Component {
    static template = "owl_playground.playground";
    static components = {Counter,Todolist,Card}
}
