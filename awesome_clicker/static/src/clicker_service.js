/** @odoo-module **/

import { reactive, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";

const clickerService = {
    start() {
        // Load state from localStorage or initialize default state
        const loadState = () => {
            try {
                const savedState = browser.localStorage.getItem('awesome_clicker_state');
                if (savedState) {
                    return JSON.parse(savedState);
                }
            } catch (error) {
                console.warn('Failed to load clicker state from localStorage:', error);
            }
            // Return default state if loading fails or no saved state exists
            return {
                clicks: 0,
                level: 0,
                clickBots: 0,
                bigBots: 0,
                quantumBots: 0,
                specialBots: 0,
                power: 1
            };
        };

        const state = reactive(loadState());
        
        // Save state to localStorage
        const saveState = () => {
            try {
                const stateToSave = {
                    clicks: state.clicks,
                    level: state.level,
                    clickBots: state.clickBots,
                    bigBots: state.bigBots,
                    quantumBots: state.quantumBots,
                    specialBots: state.specialBots,
                    power: state.power
                };
                browser.localStorage.setItem('awesome_clicker_state', JSON.stringify(stateToSave));
            } catch (error) {
                console.warn('Failed to save clicker state to localStorage:', error);
            }
        };
        
        // Set up bot income and state saving interval
        setInterval(() => {
            // Generate bot income
            if (state.clickBots > 0 || state.bigBots > 0 || state.quantumBots > 0 || state.specialBots > 0) {
                const clickBotIncome = 10 * state.clickBots * state.power;
                const bigBotIncome = 100 * state.bigBots * state.power;
                
                // QuantumBots scale with power²
                const quantumBotIncome = 50 * state.quantumBots * (state.power * state.power);
                
                // SpecialBots have critical hit chance (20% chance for 5x income)
                let specialBotIncome = 25 * state.specialBots * state.power;
                if (state.specialBots > 0 && Math.random() < 0.2) {
                    specialBotIncome *= 5; // Critical hit!
                }
                
                state.clicks += clickBotIncome + bigBotIncome + quantumBotIncome + specialBotIncome;
            }
            
            // Save state every 10 seconds
            saveState();
        }, 10000); // 10 seconds
        
        return {
            state,
            increment(inc) {
                const oldClicks = state.clicks;
                state.clicks += inc;
                
                // Check for level ups - allow jumping multiple levels
                if (state.clicks >= 10000000 && state.level < 5) {
                    state.level = 5; // SpecialBots unlock
                } else if (state.clicks >= 1000000 && state.level < 4) {
                    state.level = 4; // QuantumBots unlock
                } else if (state.clicks >= 100000 && state.level < 3) {
                    state.level = 3; // Power unlock
                } else if (state.clicks >= 5000 && state.level < 2) {
                    state.level = 2; // BigBots unlock
                } else if (state.clicks >= 1000 && state.level < 1) {
                    state.level = 1; // ClickBots unlock
                }
                
                // Save state immediately on important changes
                saveState();
            },
            buyClickBot() {
                if (state.clicks >= 1000) {
                    state.clicks -= 1000;
                    state.clickBots += 1;
                    saveState();
                }
            },
            buyBigBot() {
                if (state.clicks >= 5000) {
                    state.clicks -= 5000;
                    state.bigBots += 1;
                    saveState();
                }
            },
            buyQuantumBot() {
                if (state.clicks >= 250000) {
                    state.clicks -= 250000;
                    state.quantumBots += 1;
                    saveState();
                }
            },
            buySpecialBot() {
                if (state.clicks >= 2000000) {
                    state.clicks -= 2000000;
                    state.specialBots += 1;
                    saveState();
                }
            },
            buyPower() {
                if (state.clicks >= 50000) {
                    state.clicks -= 50000;
                    state.power += 1;
                    saveState();
                }
            },
            reset() {
                state.clicks = 0;
                state.level = 0;
                state.clickBots = 0;
                state.bigBots = 0;
                state.quantumBots = 0;
                state.specialBots = 0;
                state.power = 1;
                saveState();
            }
        };
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);

export function useClicker() {
    const clicker = useService("awesome_clicker.clicker");
    const state = useState(clicker.state);
    
    return {
        state,
        increment: clicker.increment.bind(clicker),
        buyClickBot: clicker.buyClickBot.bind(clicker),
        buyBigBot: clicker.buyBigBot.bind(clicker),
        buyQuantumBot: clicker.buyQuantumBot.bind(clicker),
        buySpecialBot: clicker.buySpecialBot.bind(clicker),
        buyPower: clicker.buyPower.bind(clicker),
        reset: clicker.reset.bind(clicker)
    };
}
