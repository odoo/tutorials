import { Component } from "@odoo/owl"

export class TodoItem extends Component {

       static template = "awesome_owl.TodoItem";

       static props = {

         todo: {
               type: Object,
               shape: { id: Number, description: String, isCompleted: Boolean }
         },
         togleState: Function,
         removeTodo: Function,

       };
      onChange(){
          this.props.togleState(this.props.todo.id)
      } 

      onRemove(){
        this.props.removeTodo(this.props.todo.id)
      }

}
