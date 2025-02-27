export const state_migrations = [
    {
        from: 1,
        to: 2,
        apply(state) {
            state.trees.pears = 0;
            state.fruits.pears = 0;
            return state;
        }
    }
]
