/** @odoo-module */

import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    let ref = useRef(name);

    onMounted(() => {
        (el) => el && el.focus(),
        () => [ref.el]
    });
  }
