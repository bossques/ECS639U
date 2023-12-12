<template>
    <div v-for="article in articleStore.articles">
        <Article :article="article" />
    </div>
</template>

<script setup lang="ts">
import { useArticleStore } from "@/store/articles.ts";
import Article from "@/components/Article.vue";
const articleStore = useArticleStore()
</script>

<style scoped>
</style>
