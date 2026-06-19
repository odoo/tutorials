import { Component, onWillStart, useState } from "@odoo/owl";

export class UsersList extends Component {
    static template = "vanilla_js.UsersList";

    setup() {
        this.state = useState({selectedUser : null, data: []})
        onWillStart(async () => {
            this.response = await fetch("https://jsonplaceholder.typicode.com/users");
            this.state.data = await this.response.json();
        });
    }

    openModal = (userId) => {
        this.state.selectedUser = this.state.data.find((user)=> user.id === userId)
        const modal = new bootstrap.Modal(document.getElementById('userModal'));
        this.cu = this.state.selectedUser
        modal.show();
    }
}
