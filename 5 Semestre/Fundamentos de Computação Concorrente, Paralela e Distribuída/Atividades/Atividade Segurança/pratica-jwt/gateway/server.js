const express = require('express');
const { expressjwt: jwt } = require('express-jwt');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 8000;

// Chave compartilhada (em produção, use variável de ambiente)
const SECRET_KEY = process.env.JWT_SECRET || 'MINHA_CHAVE_DE_ASSINATURA';
const SERVICE_B_URL = process.env.SERVICE_B_URL || 'http://localhost:4000';

app.use(cors());
app.use(express.json());

// Middleware de logging
app.use((req, res, next) => {
  console.log(`\n[${new Date().toISOString()}] ${req.method} ${req.path}`);
  console.log('Authorization header:', req.headers.authorization || 'Nenhum token fornecido');
  next();
});

// Rota de status (não protegida)
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'api-gateway',
    protected: false
  });
});

// Middleware JWT - protege todas as rotas exceto /health
const jwtMiddleware = jwt({
  secret: SECRET_KEY,
  algorithms: ['HS256'],
  credentialsRequired: true
}).unless({ path: ['/health'] });

// Handler de erros JWT customizado
app.use((err, req, res, next) => {
  if (err.name === 'UnauthorizedError') {
    console.log('❌ Erro de autenticação:', err.message);
    
    let errorMessage = 'Token inválido ou ausente';
    
    if (err.message.includes('No authorization token')) {
      errorMessage = 'Token não fornecido. Use: Authorization: Bearer <token>';
    } else if (err.message.includes('jwt expired')) {
      errorMessage = 'Token expirado. Gere um novo token.';
    } else if (err.message.includes('invalid token')) {
      errorMessage = 'Token inválido. Verifique a assinatura.';
    } else if (err.message.includes('jwt malformed')) {
      errorMessage = 'Token mal formatado.';
    }
    
    return res.status(401).json({
      error: 'Não autorizado',
      message: errorMessage,
      details: err.message
    });
  }
  next(err);
});

// Aplicar JWT middleware
app.use(jwtMiddleware);

// Middleware de sucesso na validação
app.use((req, res, next) => {
  if (req.auth) {
    console.log('✅ Token válido! Payload:', req.auth);
  }
  next();
});

// Proxy para service-b - rota protegida
app.use('/minha-rota', createProxyMiddleware({
  target: SERVICE_B_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/minha-rota': '/minha-rota'
  },
  onProxyReq: (proxyReq, req, res) => {
    console.log('🔄 Encaminhando requisição para:', SERVICE_B_URL + '/minha-rota');
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log('✅ Resposta recebida do service-b:', proxyRes.statusCode);
  },
  onError: (err, req, res) => {
    console.error('❌ Erro no proxy:', err.message);
    res.status(500).json({
      error: 'Erro ao conectar com service-b',
      details: err.message
    });
  }
}));

// Proxy para dados sensíveis - rota protegida
app.use('/dados-sensiveis', createProxyMiddleware({
  target: SERVICE_B_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/dados-sensiveis': '/dados-sensiveis'
  },
  onProxyReq: (proxyReq, req, res) => {
    console.log('🔄 Encaminhando requisição para:', SERVICE_B_URL + '/dados-sensiveis');
  }
}));

// Rota catch-all para rotas não encontradas
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Rota não encontrada',
    availableRoutes: [
      'GET /health (não protegida)',
      'GET /minha-rota (protegida com JWT)',
      'GET /dados-sensiveis (protegida com JWT)'
    ]
  });
});

app.listen(port, () => {
  console.log(`🛡️  API Gateway com JWT ativo na porta ${port}`);
  console.log(`🔑 Secret key configurada: ${SECRET_KEY.substring(0, 10)}...`);
  console.log(`📡 Proxy para service-b: ${SERVICE_B_URL}`);
  console.log(`\n📍 Rotas disponíveis:`);
  console.log(`   - GET http://localhost:${port}/health (não protegida)`);
  console.log(`   - GET http://localhost:${port}/minha-rota (protegida)`);
  console.log(`   - GET http://localhost:${port}/dados-sensiveis (protegida)`);
  console.log(`\n💡 Exemplo de uso:`);
  console.log(`   curl -H "Authorization: Bearer <seu-token>" http://localhost:${port}/minha-rota`);
});
