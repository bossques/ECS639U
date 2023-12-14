import { defineStore } from "pinia";
import type { Article, ArticleCategory } from "@/types.ts";

export const useArticleStore = defineStore('article', {
    state: () => {
        return {
            articles: [] as Article[],
            categories: [] as ArticleCategory[]
        }
    },
    actions: {
        async populate() {
            const response = await fetch('http://127.0.0.1:8000/api/articles/')
            if (response.ok) {
                const json = await response.json()
                this.articles = json['articles']
                this.categories = json['categories']
            }
        }
    }
})