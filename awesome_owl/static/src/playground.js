import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = {Counter, Card};

    setup() {
        this.state = useState({sum: 0});
        this.htmlContent = markup("<b>This Text is bold</b><br/><i>This Text is Italic</i>");
        this.state = useState({
            tasks: [
                {id: 1, name: "Learn OWL"},
                {id: 2, name: "Complete Chapter"},
                {id: 3, name: "Start doing Tasks"}
            ]
        });
    }

    incrementSum(value){
        this.state.sum += 1;
    }

    addTask(){
        const newId = this.state.tasks.length + 1;

        this.state.tasks.push({
            id: newId,
            name: "New Task " + newId,
        })
    }


}
