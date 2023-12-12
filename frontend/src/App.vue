<template>
    <NavigationBar />
    <main class="container pt-4">
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { RouterView } from "vue-router";
import NavigationBar from "./components/NavigationBar.vue";
import { useUserStore } from "@/store/userStore";

export default {
    components: {
        NavigationBar,
        RouterView
    },
    async mounted() {
        const userStore = useUserStore()
        await userStore.populate()
    }
}

</script>
