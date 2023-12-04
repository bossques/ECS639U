<template>
    {{ JSON.stringify(userStore.user) }}
</template>

<script setup lang="ts">
    import { useUserStore } from "@/store/userStore";
    const userStore = useUserStore();
</script>