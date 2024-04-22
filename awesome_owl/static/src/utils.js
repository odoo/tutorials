/** @odoo-module **/

import { useRef, useEffect } from "@odoo/owl";

export function useAutoFocus(inputRef){
    const ref = useRef(inputRef)
    useEffect(
        (el) => {
            el.focus()
        },
        () => [ref.el],
    )
}