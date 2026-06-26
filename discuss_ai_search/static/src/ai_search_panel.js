import { Component } from "@odoo/owl";
import { ActionPanel } from "@mail/discuss/core/common/action_panel";
import { useState } from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {MessageCardList} from "@mail/core/common/message_card_list";
import { markup } from "@odoo/owl";

export class AiSearchPanel extends Component {
    static template = "discuss_ai_search.AiSearchPanel";
    static props = ["thread"];
    static components = { ActionPanel, MessageCardList };
    

    setup() {
        this.orm = useService("orm");
        this.store = useService("mail.store");
        this.state = useState({
            user_prompt: "",
            answer: "",
            messageIds: [],
        });

    }
    async ask() {
        this.state.answer = ""
        this.state.messageIds = []
        const [answer, storeData, messageIds] = await this.orm.call(
            "discuss.channel",
            "action_ask_ai",
            [this.props.thread.id, this.state.user_prompt]
        )
        this.store.insert(storeData)
        this.state.answer = answer
        this.state.messageIds = messageIds
    }

    get messages() {
        return this.state.messageIds.map((id) => this.store["mail.message"].get(id)).filter(Boolean)
    }

    async summarize() {
        this.state.user_prompt = ""
        this.state.messageIds = []
        this.state.answer = ""
        const summarize = await this.orm.call(
            "discuss.channel",
            "action_summarize_ai",
            [this.props.thread.id]
        )
        this.state.answer = markup(summarize)
        
    }
}