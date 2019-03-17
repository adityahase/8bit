var App = new Vue({
    el: '#app',
    template: `
        <div class="bg-light">
            <div class="flex">
            <div class="w-1/2 h-screen">
                <h3>Registers</h3>
                <div v-for="(m, i) in states[current].registers">
                    {{i}} : <input class="border" type="number" v-model.number="states[current].registers[i]" />
                </div>
                <div>A: <input class="border" type="number" v-model.number="states[current].registers.A" /></div>
                <h3>Memory</h3>
                <div v-for="(m, i) in states[current].memory">
                    M : <input class="border" type="number" v-model.number="states[current].memory[i]" />
                </div>
            </div>
            <div class="w-1/2 bg-grey-lighter h-screen">
                <div @click="setState(h)" v-for="h in history">
                {{ h.program }}
                </div>
                <textarea class="border" cols="40" rows="10" @keydown.enter="submit"></textarea>
            </div>
            </div>
        </div>
    `,
    data() {
        return {
            states: [
                {
                    registers: {
                        A: 0,
                        B: 0
                    },
                    memory: [0, 0, 0, 0],
                    }
                ],
            current: 0,
            history: []
        }
    },
    async mounted() {
        const res = await fetch('/emulate', {
            method: 'POST',
            body: "{}"
        });
        if (res.ok) {
            const response = await res.json();
            this.states = response;
        }

    },
    methods: {
        async submit(e) {
            const program = e.target.value;
            const state = {
                registers: this.states[this.current].registers,
                memory: this.states[this.current].memory,
                program: program
            };
            const res = await fetch('/emulate', {
                method: 'POST',
                body: JSON.stringify(state)
            });
            if (res.ok) {
                const response = await res.json();
                const laststate = response.slice(-1)[0];
                this.registers = laststate.registers;
                this.memory = laststate.memory;
                this.history.push({
                    program,
                    state: {
                        registers: laststate.registers,
                        memory: laststate.memory
                    }
                });
            }
        },
        setState(h) {
            this.registers = h.state.registers;
            this.memory = h.state.memory;
        }
    }
})
