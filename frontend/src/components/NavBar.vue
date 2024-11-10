<template>
  <div
    class="flex grow-0 flex-col justify-around top-20"
  >
    <div>
      <img
        class="w-[72px] h-[72px] top-0 left-0"
        alt="Profile"
        :src="user.picture"
      />
      <div
        class="top-[92px] left-0 [font-family:'Poppins-SemiBold',Helvetica] font-semibold text-white text-3xl tracking-[0] leading-[35px] whitespace-nowrap capitalize"
      >
        {{ user.role }}
      </div>

      <div
        class="top-[132px] left-0 opacity-60 [font-family:'Poppins-Regular',Helvetica] font-normal text-white text-[17px] tracking-[0] leading-[27px] whitespace-nowrap"
      >
        {{ user.email }}
      </div>
    </div>

    <div>
      <v-for>
        <RouterLink v-for="r in routes" :key="r.path" :to="r.path">
          <div
            class="opacity-50 font-family:'Poppins-SemiBold',Helvetica] font-semibold text-white text-[25px] tracking-[0] leading-[35px] whitespace-nowrap"
          >
            {{ r.name }}
          </div>
        </RouterLink>
      </v-for>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'NavBar',
  computed: {
    ...mapState(['user']),
    routes() {
      return this.$router
        .getRoutes()
        .filter(r => Object.prototype.hasOwnProperty.call(r.meta, 'home'))
    },
  },
  props: {
    sidebarType: String,
  },
}
</script>
<style>
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  height: 100%;
  width: 100%;
}
</style>