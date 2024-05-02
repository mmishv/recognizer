import HttpClient from '@/api/HttpClient'
import { FormulaInput } from '@/domain/entities/formulaInput'
import { Formula } from '@/domain/entities/formula'

export default class RecognizerApi extends HttpClient {
  private readonly API_URL: string = import.meta.env.VITE_CALCULATOR_API_URL!

  async recognizeFormula(data: FormulaInput): Promise<Formula> {
    const formData = new FormData()
    formData.append('image', data.image)
    let result = await this.fetchData(`${this.API_URL}/v1/recognizer/`, 'POST', formData)
    return this.mapFormula(result.body)
  }

  private mapFormula(data: any): Formula {
    return {
      image: data.image,
      expression: data.expression
    }
  }
}
