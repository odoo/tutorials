/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

import {TodoList} from './todo/todo_list'


export class Playground extends Component {
    static template = "awesome_owl.playground";
    
    //tut 1- 6
    setup() {
        this.state = useState({ 
            content: markup("<h1>hello</h1>"),
            sum: 0
        });
    }

    incrementSum() {
        this.state.sum++;
    }
    

    //tut 7
    static components = {Counter, Card, TodoList}

}
