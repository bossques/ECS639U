export type ErrorMessage = {
    message: string;
    code: string;
}

export type BadRequestResponse = Record<string, ErrorMessage[]>

export type User = {
    id: number
    email: string
    username: string
    date_of_birth: string
    profile_image?: string | null,
    favourite_categories: ArticleCategory[]
}

export type ArticleCategory = {
    id: number
    name: string
}

export type Article = {
    id: number
    category: ArticleCategory
    title: string
    contents: string
    created_at: string
}

export type ArticleComment = {
    id: number
    article: Article
    belongs_to: User
    comment: string
    reply_to?: ArticleComment
    created_at: string
}

export type NestedArticleComment = ArticleComment & {
    replies: NestedArticleComment[]
}