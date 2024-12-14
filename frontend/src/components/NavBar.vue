<script setup>
import { Button } from 'primevue'
</script>
<template>
  <div class="flex grow-0 flex-col justify-around ps-10">
    <div>
      <!-- Back Button -->
      <div v-if="sidebarType === 'project'" class="absolute top-4 left-4">
        <Button
          icon="pi pi-arrow-left"
          label="Back"
          class="p-button-text text-white"
          @click="goBack"
        />
      </div>
      <div
        class="top-[92px] left-0 [font-family:'Poppins-SemiBold',Helvetica] font-semibold text-white text-3xl tracking-[0] leading-[35px] whitespace-nowrap capitalize"
      >
        {{ user.role }}
        <span>
          <Button
            icon="pi pi-sign-out"
            severity="danger"
            variant="text"
            rounded
            aria-label="Cancel"
            @click="
              () => {
                store.commit('logout')
                this.$router.push('/login')
              }
            "
          />
        </span>
      </div>

      <div
        class="top-[132px] left-0 opacity-60 [font-family:'Poppins-Regular',Helvetica] font-normal text-white text-[17px] tracking-[0] leading-[27px] whitespace-nowrap"
      >
        {{ user.email }}
      </div>
    </div>

    <div>
      <RouterLink 
        v-for="r in routes" 
        :key="r.path" 
        :to="{name: r.name, params: {projectId: projectId}}"
        :class="[$route.name === r.name ? 'opacity-100' : 'opacity-50']"
      >

        <div
          :class="[
            'font-family:\'Poppins-SemiBold\',Helvetica',
            'font-semibold',
            'text-white',
            'text-[25px]',
            'tracking-[0]',
            'leading-[35px]',
            'whitespace-nowrap',
          ]"
        >
          {{ r.name }}
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import store from '@/store';

export default {
  name: 'NavBar',
  computed: {
    ...mapState(['user']),
    routes() {
      return this.$router
        .getRoutes()
        .filter(r => Object.prototype.hasOwnProperty.call(r.meta, this.sidebarType))
        .filter(r => Object.prototype.hasOwnProperty.call(r.meta, this.user.role))
    },
  },
  props: {
    sidebarType: {
      type: String,
      default: 'home',
      required: true
    },
    projectId: {
      type: String,
      default: null,
      required: false
    }
  },
  methods: {
    goBack() {
      this.$router.push({ name: 'Projects' });
    },
  },
}
</script>
