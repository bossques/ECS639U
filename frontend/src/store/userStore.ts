import { defineStore } from "pinia";

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
        async modify(formData: FormData) {
            const response = await fetch('http://127.0.0.1:8000/api/profile/', {
                'method': 'PUT',
                'body': formData
            })

            if(response.ok) {
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

function getCookie(name: string): string | undefined {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop()?.split(';').shift()?.trim();
    }
    return undefined;
}

interface User {
    id: Number
    username: String
    profile_url?: String
}