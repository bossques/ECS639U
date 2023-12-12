import { defineStore } from "pinia";
import type {ArticleCategory, BadRequestResponse, User} from "@/types.ts";

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            user: null as User | null,
        }
    },
    actions: {
        async populate() {
            const response = await fetch('http://127.0.0.1:8000/api/profile/')
            if (response.ok) {
                this.user = await response.json()
            }
        },
        async modify(email: string, dateOfBirth: string, profileImage: File | null) {
            // if csrf token is found in cookies, add to header
            const headers: Record<string, string> = {};
            const token = getCookie('csrftoken')
            if (token !== undefined) {
                headers['X-CSRFToken'] = token;
            }

            const formData = new FormData()
            formData.append('email', email)
            formData.append('date_of_birth', dateOfBirth)
            if (profileImage != null) {
                formData.append('profile_image', profileImage, profileImage.name)
            }

            const response = await fetch('http://127.0.0.1:8000/api/profile/', {
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
            // if csrf token is found in cookies, add to header
            const headers: Record<string, string> = {};
            const token = getCookie('csrftoken')
            if (token !== undefined) {
                headers['X-CSRFToken'] = token;
            }

            const response = await fetch(`http://127.0.0.1:8000/api/profile/categories/${category.id}/`, {
                'method': 'PUT',
                'headers': headers
            })

            if (response.ok) {
                this.user = await response.json()
            }
        },
        async logout() {
            // if csrf token is found in cookies, add to header
            const headers: Record<string, string> = {};
            const token = getCookie('csrftoken')
            if (token !== undefined) {
                headers['X-CSRFToken'] = token;
            }

            const response = await fetch('http://127.0.0.1:8000/auth/logout/', {
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

function getCookie(name: string): string | undefined {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop()?.split(';').shift()?.trim();
    }
    return undefined;
}