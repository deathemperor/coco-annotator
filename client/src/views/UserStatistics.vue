<template>
  <div>
    <div style="padding-top: 55px" />
    
    <div class="bg-light">
      <div class="bg-light text-left" style="overflow: auto; height: calc(100vh - 100px); margin: 10px">

        <div class="container">

          <div style="width: 100%">
            <div style="float: left;">From Date: <datepicker v-model="startDate" :format="customFormatter" /></div>
            <div style="float: left">To Date: <datepicker v-model="endDate" :format="customFormatter" /></div>
            <div style="float: left; padding-left: 20px; padding-top: 10px"><button @click="loadData()">Load Data</button></div>
          </div>
          <table class="table table-hover table-sm">
            <thead class="remove-top-border">
              <tr>
                <th scope="col">Date</th>
                <th class="text-center" scope="col">Completed Images</th>
                <th class="text-center" scope="col">Verified Images</th>
                <th class="text-center" scope="col">Rejected Images</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(stat, index) in stats" :key="index" style="cursor: pointer" @click="viewDetail(username, stat.day)">
                <td>{{ stat.day }}</td>
                <td class="text-center">
                  {{ stat.completedCount }}
                </td>
                <td class="text-center">
                  {{ stat.verifiedCount }}
                </td>
                <td class="text-center">
                  {{ stat.rejectedCount }}
                </td>
              </tr>
            </tbody>
          </table>


        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Datepicker from 'vuejs-datepicker';
import moment from "moment";


export default {
  name: "Statistics",
  components: {
    Datepicker
  },
  data() {
    return {
      stats: [],
      startDate: moment().startOf('month').format('YYYY-MM-DD'),
      endDate: moment().endOf('month').format('YYYY-MM-DD'),
    };
  },
  props: {
    username: {
      type: String,
      required: true
    }
  },
  methods: {
    viewDetail(username, date) {
      this.$router.push({name: 'userImages', params: { username: this.username, date: date }});
    },
    customFormatter(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    loadData() {
      this.stats = [];
      axios.get(`/api/user/${this.username}/stats?start_date=${this.customFormatter(this.startDate)}&end_date=${this.customFormatter(this.endDate)}`)
        .then((response) => {
          const data = response.data;
          for (let stat in data.stats) {
            this.stats.push(data.stats[stat])
          }
        });
    }
  },
  created() {
    this.loadData()
  }
};
</script>
