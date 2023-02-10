export default {
    data() {
      return {
        services: {},
        redScore: 40,
        blueScore: 60,
        totalScore: this.blueScore + this.redScore
      }
    },
    created() {
        this.getData();
        this.timer = setInterval(this.getData, 30000);
    },
    methods:
    {
        async getData() {
            console.log("Fetching");
            let response = await fetch("http://127.0.0.1:5000/display_scores");
            this.services = await response.json();
            let totalScore = this.blueScore + this.redScore;

            document.getElementById('score').style.background=`linear-gradient(to right, blue ${this.blueScore / totalScore}, red ${this.redScore / totalScore})`
        },
        cancelUpdates() {
            clearInterval(this.timer);
        },
        updateScore1(){
            this.blueScore += 5;
            let totalScore = this.blueScore + this.redScore;
            document.getElementById('score').style.background=`linear-gradient(to right, blue ${this.blueScore / totalScore}, red ${this.redScore / totalScore})`

            // let bar = document.getElementById('score');
            // bar.style.background=`linear-gradient(to right, blue ${this.blueScore / totalScore}, red ${this.redScore / totalScore} )`
        },
        updateScore2() {
            this.redScore += 5;
            let totalScore = this.blueScore + this.redScore;

            let bar = document.getElementById('score');
            console.log(bar);
            bar.style.background=`linear-gradient(to right, blue ${this.blueScore / totalScore}, red ${this.redScore / totalScore} )`
        }
    },
    computed: {
        createBackgroundString() {
            console.log(`linear-gradient(to right, blue ${this.blueScore}, red ${this.redScore})`);
            return `linear-gradient(to right, blue ${this.blueScore}, red ${this.redScore})`;
        }
    },
    beforeUnmount() {
        this.cancelUpdates();
    },
    template: `
    <div class="scoring">
    <p style="text-align:left; padding-left:20px">
    {{blueScore}}
        <span style="float:right; padding-right:20px"> {{redScore}} </span>
 
    </p> 
    <div class="scoreBar" id="score" :style={background:}></div>
    </div>

    <div v-for="host, key in services">
    {{key}}
        <table>
        <tr>
            <th> Service </th>
            <th> Status </th>
        </tr>
        <tr v-for="status, service in host">
            <td> {{service}} </td> 
            <td> {{status}}  </td>
        </tr>
        </table>
        <br/>
    </div>
    <button @click="updateScore1"> click me!</button>
    <button @click="updateScore2"> click me2!</button>
    `
  }

