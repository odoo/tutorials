import { Component, type, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card}
    

    taskDone (param){
        debugger;
        this.obj.tasks.forEach((task)=>{
            if(task == param){
                task.status = true;
            }
        })
    }

    setup(){
        this.obj = useState({tasks: [{type: Object}]});
        this.obj.tasks = [
            {'task': "add color", "status":true},
            {'task': "code", "status":true},
            {'task': "code1", "status":true},
            {'task': "code2", "status":false},
            {'task': "code3", "status":false},
            {'task': "code4", "status":false},
            {'task': "code5", "status":false}
        ]

        console.log(this);
    }
}
