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
    profile_url?: string | null
}