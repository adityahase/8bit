var App = new Vue({
    el: '#app',
    template: `
        <div class="bg-light">
            <div class="flex">
            <div class="w-3/4 h-screen">
                <h3>Registers</h3>
                <table class="table-fixed text-center">
                    <thead>
                        <tr>
                            <th v-for="(m, i) in states[current].registers">{{i}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td v-for="(m, i) in states[current].registers"><input class="border w-12 text-right" v-model.number="states[current].registers[i]"/></td>
                        </tr>
                    </tbody>
                </table>
                <h3>Memory</h3>
                <div v-for="chunk in [...Array(16).keys()]">
                    <span v-for="(m, i) in states[current].memory.slice(chunk*16, chunk*16 + 16)">
                        <input class="border w-12 text-right" v-model.number="states[current].memory[chunk*16+i]" />
                    </span>
                </div>
            </div>
            <div class="w-1/4 bg-grey-lighter h-screen">
                <textarea class="border" cols="40" rows="10" @keydown.meta.enter="submit"></textarea>
            </div>
            </div>
        </div>
    `,
    data() {
        return {
            states: [
                {
                    registers: {},
                    memory: [],
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
                this.states = response;
                this.current = this.states.length - 1;

                // const laststate = response.slice(-1)[0];
                // console.log(laststate);
                // this.history.push({
                //     program,
                //     state: {
                //         registers: laststate.registers,
                //         memory: laststate.memory
                //     }
                // });
            }
        },
        // setState(h) {
        //     console.log(h);
        //     this.registers = h.state.registers;
        //     this.memory = h.state.memory;
        // }
    }
})
