import { useState, useRef, useEffect } from 'react'
import { MessageCircle, X, Send, Bot, User, Loader2, ChevronUp, ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent } from '@/components/ui/card.jsx'

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Detectar se estamos em produção ou desenvolvimento
  const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://api.guvito.site'

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  const addMessage = (content, isUser = false, type = 'text') => {
    const newMessage = {
      id: Date.now(),
      content,
      isUser,
      type,
      timestamp: new Date().toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    }
    setMessages(prev => [...prev, newMessage])
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage = inputValue.trim()
    setInputValue('')
    addMessage(userMessage, true)

    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/chat/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage }),
      })

      const data = await response.json()

      if (response.ok) {
        addMessage(data.response, false, data.type || 'text')
      } else {
        addMessage(`❌ Erro: ${data.error || 'Erro desconhecido'}`, false, 'error')
      }
    } catch (error) {
      addMessage('❌ Erro de conexão. Verifique se o backend está rodando.', false, 'error')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const formatMessage = (content, type) => {
    if (type === 'error') {
      return <span className="text-red-600">{content}</span>
    }
    
    // Converter markdown simples para HTML
    const formattedContent = content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br />')
    
    return <div dangerouslySetInnerHTML={{ __html: formattedContent }} />
  }

  const getSuggestions = () => [
    "Mostre as mudanças no estoque",
    "Histórico da peça A 0001808909",
    "Análise de localizações",
    "Insights gerais do estoque"
  ]

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion)
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Chat Widget */}
      <div className={`transition-all duration-300 ease-in-out ${isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'}`}>
        <Card className="w-96 h-[500px] shadow-2xl border-2 border-blue-200">
          <CardContent className="p-0 h-full flex flex-col">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-t-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Bot className="h-5 w-5" />
                  <h3 className="font-semibold">Assistente de Estoque</h3>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                  className="text-white hover:bg-blue-600"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-sm text-blue-100 mt-1">
                Faça perguntas sobre as planilhas de estoque
              </p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
              {messages.length === 0 && (
                <div className="text-center text-gray-500 py-8">
                  <Bot className="h-12 w-12 mx-auto mb-3 text-blue-400" />
                  <p className="text-sm">Olá! Sou seu assistente de estoque.</p>
                  <p className="text-xs mt-1">Posso analisar planilhas e responder suas perguntas.</p>
                  
                  {/* Suggestions */}
                  <div className="mt-4 space-y-2">
                    <p className="text-xs font-medium text-gray-600">Sugestões:</p>
                    {getSuggestions().map((suggestion, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="block w-full text-left text-xs bg-white border border-gray-200 rounded-lg px-3 py-2 hover:bg-blue-50 hover:border-blue-200 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-3 py-2 ${
                      message.isUser
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-gray-200'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      {!message.isUser && (
                        <Bot className="h-4 w-4 mt-0.5 text-blue-500 flex-shrink-0" />
                      )}
                      <div className="flex-1">
                        <div className="text-sm">
                          {formatMessage(message.content, message.type)}
                        </div>
                        <div className={`text-xs mt-1 ${
                          message.isUser ? 'text-blue-100' : 'text-gray-400'
                        }`}>
                          {message.timestamp}
                        </div>
                      </div>
                      {message.isUser && (
                        <User className="h-4 w-4 mt-0.5 text-blue-100 flex-shrink-0" />
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 rounded-lg px-3 py-2">
                    <div className="flex items-center gap-2">
                      <Bot className="h-4 w-4 text-blue-500" />
                      <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
                      <span className="text-sm text-gray-600">Analisando...</span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200 bg-white">
              <div className="flex gap-2">
                <Input
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Digite sua pergunta..."
                  className="flex-1"
                  disabled={isLoading}
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  size="sm"
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Chat Toggle Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 shadow-lg border-2 border-white"
      >
        {isOpen ? (
          <ChevronDown className="h-6 w-6" />
        ) : (
          <MessageCircle className="h-6 w-6" />
        )}
      </Button>
    </div>
  )
}

export default ChatWidget 