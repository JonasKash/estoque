import { useState, useEffect } from 'react'
import { Search, Package, MapPin, Hash, BarChart3, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)

  // Detectar se estamos em produção ou desenvolvimento
  const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:5000'
  : 'https://api.guvito.site';

  const searchStock = async () => {
    if (!query.trim()) return
    
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
      
      const data = await response.json()
      setResults(data.results || [])
    } catch (error) {
      console.error('Erro na busca:', error)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`)
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
    }
  }

  // Carregar estatísticas ao inicializar
  useEffect(() => {
    loadStats()
  }, [])

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchStock()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-3">
            <Package className="h-10 w-10 text-blue-600" />
            Sistema de Consulta de Estoque
          </h1>
          <p className="text-lg text-gray-600">
            Faça perguntas sobre quantidade, localização e número de peças
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total de Itens</CardTitle>
                <Package className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_items}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Quantidade Total</CardTitle>
                <BarChart3 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_quantity}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Localizações Únicas</CardTitle>
                <MapPin className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.unique_locations}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Search Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Buscar no Estoque
            </CardTitle>
            <CardDescription>
              Digite o nome da peça, número ou localização que você está procurando
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2">
              <Input
                placeholder="Ex: filtro de óleo, A 0001808909, estrado 5..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1"
              />
              <Button onClick={searchStock} disabled={loading}>
                {loading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Search className="h-4 w-4" />
                )}
                Buscar
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        {results.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Resultados da Busca</CardTitle>
              <CardDescription>
                Encontrados {results.length} itens para "{query}"
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {results.map((item, index) => (
                  <div
                    key={index}
                    className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Hash className="h-4 w-4 text-gray-500" />
                          <code className="text-sm font-mono bg-gray-100 px-2 py-1 rounded">
                            {item['Numero da Peca']}
                          </code>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-1">
                          {item.Descricao}
                        </h3>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <div className="flex items-center gap-1">
                            <Package className="h-4 w-4" />
                            <span>Qtd: {item.Quantidade}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            <span>Local: {item.Localizacao}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Badge variant="secondary">
                          {item.Quantidade} unidades
                        </Badge>
                        <Badge variant="outline">
                          {item.Localizacao}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Examples Section */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Exemplos de Consultas</CardTitle>
            <CardDescription>
              Experimente estas consultas para ver como o sistema funciona
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <h4 className="font-semibold">Por Descrição:</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "filtro de óleo"</li>
                  <li>• "junta de borracha"</li>
                  <li>• "sensor de pressão"</li>
                </ul>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold">Por Localização:</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "estrado 5"</li>
                  <li>• "lubri"</li>
                  <li>• "21D18"</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App

