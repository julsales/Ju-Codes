const express = require('express');
const fetch = require('node-fetch');
const jwt = require('jsonwebtoken');
const app = express();
const port = process.env.PORT || 3000;

// Chave compartilhada (em produção, use variável de ambiente)
const SECRET_KEY = 'MINHA_CHAVE_DE_ASSINATURA';
const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:8000';
const SERVICE_B_DIRECT_URL = 'http://localhost:4000';

app.use(express.json());

// Função para gerar token JWT
function generateToken(expiresIn = '30s') {
  return jwt.sign(
    { 
      service: 'service-a',
      timestamp: new Date().toISOString()
    }, 
    SECRET_KEY, 
    { expiresIn }
  );
}

// Rota de status
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'service-a' });
});

// Chamada direta ao service-b (sem gateway, sem token)
app.get('/call-direct', async (req, res) => {
  try {
    console.log('📞 Chamando service-b diretamente (sem gateway, sem token)...');
    const response = await fetch(`${SERVICE_B_DIRECT_URL}/minha-rota`);
    const body = await response.json();
    
    res.json({ 
      from: 'service-a',
      method: 'direct-call (sem proteção)',
      serviceB: body,
      status: response.status
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Erro ao chamar service-b diretamente',
      details: error.message 
    });
  }
});

// Chamada através do gateway SEM token (deve falhar)
app.get('/call-gateway-no-token', async (req, res) => {
  try {
    console.log('📞 Chamando service-b via gateway SEM token...');
    const response = await fetch(`${GATEWAY_URL}/minha-rota`);
    const body = await response.json();
    
    res.json({ 
      from: 'service-a',
      method: 'gateway-call (sem token)',
      serviceB: body,
      status: response.status
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Erro ao chamar gateway sem token',
      details: error.message 
    });
  }
});

// Chamada através do gateway COM token válido
app.get('/call-gateway-with-token', async (req, res) => {
  try {
    const token = generateToken('30s');
    console.log('📞 Chamando service-b via gateway COM token válido...');
    console.log('🔑 Token gerado:', token);
    
    const response = await fetch(`${GATEWAY_URL}/minha-rota`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const body = await response.json();
    
    res.json({ 
      from: 'service-a',
      method: 'gateway-call (com token válido)',
      token: token,
      serviceB: body,
      status: response.status
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Erro ao chamar gateway com token',
      details: error.message 
    });
  }
});

// Chamada com token expirado
app.get('/call-gateway-expired-token', async (req, res) => {
  try {
    // Gera token que expira em 1 segundo
    const token = generateToken('1s');
    console.log('📞 Aguardando 2 segundos para token expirar...');
    
    // Aguarda 2 segundos
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    console.log('📞 Chamando service-b via gateway com token EXPIRADO...');
    const response = await fetch(`${GATEWAY_URL}/minha-rota`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const body = await response.json();
    
    res.json({ 
      from: 'service-a',
      method: 'gateway-call (com token expirado)',
      token: token,
      serviceB: body,
      status: response.status
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Erro ao chamar gateway com token expirado',
      details: error.message 
    });
  }
});

// Endpoint para gerar token manualmente
app.get('/generate-token', (req, res) => {
  const expiresIn = req.query.expiresIn || '30s';
  const token = generateToken(expiresIn);
  
  res.json({
    token: token,
    expiresIn: expiresIn,
    usage: `curl -H "Authorization: Bearer ${token}" ${GATEWAY_URL}/minha-rota`
  });
});

app.listen(port, () => {
  console.log(`🚀 service-a ouvindo na porta ${port}`);
  console.log(`📍 Endpoints disponíveis:`);
  console.log(`   - GET http://localhost:${port}/call-direct`);
  console.log(`   - GET http://localhost:${port}/call-gateway-no-token`);
  console.log(`   - GET http://localhost:${port}/call-gateway-with-token`);
  console.log(`   - GET http://localhost:${port}/call-gateway-expired-token`);
  console.log(`   - GET http://localhost:${port}/generate-token?expiresIn=30s`);
  console.log(`   - GET http://localhost:${port}/health`);
});
