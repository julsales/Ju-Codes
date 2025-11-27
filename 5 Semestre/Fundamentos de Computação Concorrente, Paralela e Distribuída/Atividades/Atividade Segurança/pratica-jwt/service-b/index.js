const express = require('express');
const app = express();
const port = process.env.PORT || 4000;

app.use(express.json());

// Middleware para log de requisições
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  console.log('Headers:', req.headers);
  next();
});

// Rota principal protegida
app.get('/minha-rota', (req, res) => {
  res.json({ 
    message: 'Acesso autorizado ao service-b',
    timestamp: new Date().toISOString(),
    service: 'service-b'
  });
});

// Rota de status
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'service-b' });
});

// Rota de dados sensíveis (exemplo)
app.get('/dados-sensiveis', (req, res) => {
  res.json({
    message: 'Dados confidenciais do service-b',
    data: {
      usuarios: 1500,
      transacoes: 42000,
      receita: 'R$ 1.234.567,89'
    }
  });
});

app.listen(port, () => {
  console.log(`🚀 service-b ouvindo na porta ${port}`);
  console.log(`📍 Endpoints disponíveis:`);
  console.log(`   - GET http://localhost:${port}/minha-rota`);
  console.log(`   - GET http://localhost:${port}/dados-sensiveis`);
  console.log(`   - GET http://localhost:${port}/health`);
});
