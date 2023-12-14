import { defineStore } from "pinia";
import type { Article, ArticleCategory } from "@/types.ts";
import {getUrl} from "@/utils.ts";

export const useArticleStore = defineStore('article', {
    state: () => {
        return {
            articles: [] as Article[],
            categories: [] as ArticleCategory[]
        }
    },
    actions: {
        async populate() {
            const response = await fetch(getUrl() + 'api/articles/')
            if (response.ok) {
                const json = await response.json()
                this.articles = json['articles']
                this.categories = json['categories']
            }
        }
    }
})