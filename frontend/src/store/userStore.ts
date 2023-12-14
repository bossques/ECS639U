import { defineStore } from "pinia";
import type {ArticleCategory, BadRequestResponse, User} from "@/types.ts";
import { getHeaders, getUrl } from "@/utils.ts";

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            user: null as User | null,
        }
    },
    actions: {
        async populate() {
            const response = await fetch(getUrl() + 'api/profile/')
            if (response.ok) {
                this.user = await response.json()
            }
        },
        async modify(email: string, dateOfBirth: string, profileImage: File | null) {
            const headers = getHeaders()

            const formData = new FormData()
            formData.append('email', email)
            formData.append('date_of_birth', dateOfBirth)
            if (profileImage != null) {
                formData.append('profile_image', profileImage, profileImage.name)
            }

            const response = await fetch(getUrl() + 'api/profile/', {
                'method': 'POST',
                'headers': headers,
                'body': formData
            })

            if(response.ok) {
                this.user = await response.json()
            } else {
                const json: BadRequestResponse = await response.json()
                throw new BadRequestError(json)
            }
        },
        async toggleCategory(category: ArticleCategory) {
            const headers = getHeaders()

            const response = await fetch(getUrl() + `api/profile/categories/${category.id}/`, {
                'method': 'PUT',
                'headers': headers
            })

            if (response.ok) {
                this.user = await response.json()
            }
        },
        async logout() {
            const headers = getHeaders()

            const response = await fetch(getUrl() + 'auth/logout/', {
                'method': 'POST',
                'headers': headers
            })

            if (response.ok) {
                this.user = null
            }
        }
    }
})

export class BadRequestError extends Error {
    public readonly errors: BadRequestResponse;

    constructor(errors: BadRequestResponse) {
        super(errors.toString());
        this.name = "BadRequestError"
        this.errors = errors
    }
}