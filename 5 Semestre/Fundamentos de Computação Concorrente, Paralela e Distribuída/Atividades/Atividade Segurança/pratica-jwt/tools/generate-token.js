const jwt = require('jsonwebtoken');

// Chave compartilhada (deve ser a mesma do gateway)
const SECRET_KEY = 'MINHA_CHAVE_DE_ASSINATURA';

// Configurações
const expiresIn = process.argv[2] || '30s'; // Pode passar como argumento: node generate-token.js 60s

// Payload do token
const payload = {
  service: 'service-a',
  timestamp: new Date().toISOString(),
  purpose: 'inter-service-communication'
};

// Gerar token
const token = jwt.sign(payload, SECRET_KEY, { 
  expiresIn: expiresIn,
  algorithm: 'HS256'
});

console.log('\n🔑 JWT Token Gerado com Sucesso!\n');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('Token:');
console.log(token);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log('📋 Informações:');
console.log(`   Expira em: ${expiresIn}`);
console.log(`   Algoritmo: HS256`);
console.log(`   Payload:`, payload);

console.log('\n💡 Como usar:\n');
console.log('   # Com curl:');
console.log(`   curl -H "Authorization: Bearer ${token}" http://localhost:8000/minha-rota\n`);

console.log('   # Com PowerShell:');
console.log(`   $headers = @{ "Authorization" = "Bearer ${token}" }`);
console.log(`   Invoke-RestMethod -Uri "http://localhost:8000/minha-rota" -Headers $headers\n`);

// Decodificar token para mostrar
const decoded = jwt.decode(token, { complete: true });
console.log('🔍 Token decodificado:');
console.log('   Header:', decoded.header);
console.log('   Payload:', decoded.payload);
console.log('   Expira em:', new Date(decoded.payload.exp * 1000).toISOString());
