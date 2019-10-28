<template>
  <div>
    <div style="padding-top: 55px" />
    
    <div
      class="bg-light"
    >
    
      <div class="bg-light text-left" style="overflow: auto; height: calc(100vh - 100px); margin: 10px">

        <div class="container">

          <table class="table table-hover table-sm">
            <thead class="remove-top-border">
              <tr>
                <th scope="col">Name</th>
                <th class="text-center" scope="col">Completed Images</th>
                <th class="text-center" scope="col">Verified Images</th>
                <th class="text-center" scope="col">Rejected Images</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(user, index) in users" :key="index" style="cursor: pointer" @click="viewDetail(user.username)">
                <td>{{ user.name }} ({{ user.username }})</td>
                <td class="text-center">
                  {{ user.completed_images_total }}
                </td>
                <td class="text-center">
                  {{ user.verified_images_total }}
                </td>
                <td class="text-center">
                  {{ user.rejected_images_total }}
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

export default {
  name: "Statistics",
  data() {
    return {
      users: []
    };
  },
  methods: {
    viewDetail(username) {
      this.$router.push({name: 'userStatistics', params: {username}})
    }
  },
  watch: {},
  created() {
    axios.get('/api/user/stats')
      .then((response) => {
        this.users = response.data;
      });
  }
};
</script>
