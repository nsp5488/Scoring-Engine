export default {
    data() {
      return {
        services: {}
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
        },
        cancelUpdates() {
            clearInterval(this.timer);
        }
    },
    beforeUnmount() {
        this.cancelUpdates();
    },
    template: `
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
    `
  }

