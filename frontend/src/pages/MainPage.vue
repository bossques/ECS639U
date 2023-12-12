<template>
    <div v-for="(articles, category) in sortByCategory(articleStore.articles)">
        <h3 class="p-2">{{ category }}</h3>

        <div class="row col-sm-12">
            <div v-for="article in articles" class="col-sm-3">
                <ArticleCard :article="article" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useArticleStore } from "@/store/articles.ts";
import ArticleCard from "@/components/ArticleCard.vue";
import { Article } from "@/types.ts";
const articleStore = useArticleStore()

function sortByCategory(articles: Article[]): Record<string, Article[]> {
    const map: Record<string, Article[]> = {};

    articles.forEach(article => {
        const categoryName = article.category.name
        if (!map[categoryName]) {
            map[categoryName] = [];
        }
        map[categoryName].push(article)
    })

    return map;
}

</script>

<style scoped>
</style>
