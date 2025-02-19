import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter,Card,TodoList}

    setup(){
        this.state = useState({
            counter1 :0,
            counter2 :0,
            sum:0,
            normalText: "This is normal Text",
            htmlContent: markup("<strong>This is bold content inside HTML</strong>")
        })
    }
    incrementSum() {
        this.state.sum++
    }
}
