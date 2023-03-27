export default {
    data() {
      return {
        services: {},
        redScore: 0,
        blueScore: 0,
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
	    let body = await response.json();
	    this.services = body.services;
	    this.blueScore = body.scores.blue_score;
  	    this.redScore = body.scores.red_score;
	    this.rows = [];
	    for(let ip in this.services) {
		let host = this.services[ip]
		for(let service in host) {
		    let status = host[service]
		    console.log(host);
	       	    this.rows.push({'ip': ip, 'service': service, 'status': status})
		}
	    }
	},
        cancelUpdates() {
            clearInterval(this.timer);
        },
    },
    beforeUnmount() {
        this.cancelUpdates();
    },
    template: `
    <div class="scoring">
        <h1 style="text-align:left; padding-left:20px; color:white;">
            Blue Score: {{blueScore}}
            <span style="float:right; padding-right:20px"> Red Score: {{redScore}} </span>
        </h1> 
    </div>
    <div class='scoreTable'>
        <table>
	    <tr>
	        <th> IP </th>
	        <th> Service </th>
	        <th> Status </th>
	    </tr>

	    <tr v-for="row in rows">
	        <td> {{row.ip}} </td>
	        <td> {{row.service}} </td>
	        <td v-if='row.status=="UP"'> <span class='dotUp'></span>  </td>
	        <td v-else> <span class='dotDown'></span>  </td>
	     </tr>
        </table>
    </div>
    `
  }

