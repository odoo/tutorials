import { useRef, useEffect } from "@odoo/owl";

function useAutofocus(refname) {

    let ref = useRef(refname);
    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
    );


  }

export {
    useAutofocus
};
