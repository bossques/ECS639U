function getCookie(name: string): string | undefined {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop()?.split(';').shift()?.trim();
    }
    return undefined;
}

export function getCSRFToken(): string | undefined {
    return getCookie('csrftoken')
}

export function getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {}

    const token = getCSRFToken()
    if (token !== undefined) {
        headers['X-CSRFToken'] = token;
    }

    return headers
}

