/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(todo)
{
    let ref = useRef(todo);
    onMounted(() => ref.el && ref.el.focus());
}