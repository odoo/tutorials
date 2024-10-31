import {Clicker} from './model'

const CLICKER_KEY = 'awesome_clicker.clicker'

export function saveGame(store) {
    localStorage.setItem(CLICKER_KEY, JSON.stringify(store.state))
}

export function loadGame() {
    return new Clicker(JSON.parse(localStorage.getItem(CLICKER_KEY)))
}