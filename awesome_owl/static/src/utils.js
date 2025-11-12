import { useRef, useEffect } from "@odoo/owl"

export function useAutofocus(itemName) {
    let ref = useRef(itemName);
    useEffect(
        (el) => el?.focus(),
        () => [ref.el]
    )
}
