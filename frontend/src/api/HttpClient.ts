import APIError from '@/api/exceptions/apiExceptions'
import { FetchResult } from '@/domain/apiModels'

export default class HttpClient {
  protected async fetchData(
    url: string,
    method: string,
    body: string | FormData | null
  ): Promise<FetchResult> {
    const headers =
      body instanceof FormData
        ? undefined
        : {
            'Content-Type': 'application/json'
          }
    let errorMessage = 'Unknown error'
    try {
      const response = await fetch(url, { method, body, headers })
      const responseBody = await response.json().catch(() => null)
      if (!response.ok) {
        for (const key in responseBody) {
          if (responseBody[key]) {
            errorMessage = responseBody[key]
            break
          }
        }
        throw new APIError(errorMessage)
      }
      return {
        body: responseBody,
        status: response.status
      }
    } catch (error) {
      console.log(error)
      throw new APIError(errorMessage)
    }
  }
}
