import { useRef, useEffect } from "@odoo/owl";

export const useAutofocus = (name) => {
    let ref = useRef(name);
    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
        , [ref]);
    return ref;
}
