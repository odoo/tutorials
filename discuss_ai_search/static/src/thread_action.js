import { registerThreadAction } from "@mail/core/common/thread_actions";
import { AiSearchPanel } from "@discuss_ai_search/ai_search_panel";
import { _t } from "@web/core/l10n/translation";

registerThreadAction("discuss_ai_search", {
    actionPanelComponent: AiSearchPanel,
    condition: ({ thread }) => thread?.model === "discuss.channel",
    icon: "fa fa-fw fa-magic",
    name: _t("Ask AI"),
    sequence: 9,
    sequenceGroup: 30,
    toggle: true,
});