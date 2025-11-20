#!/usr/bin/env python3
"""
Script para gerar tokens JWT
Uso: python generate-token.py [tempo_expiracao]
Exemplo: python generate-token.py 60
"""

import jwt
import sys
from datetime import datetime, timedelta

# Chave compartilhada (deve ser a mesma do gateway)
SECRET_KEY = 'MINHA_CHAVE_DE_ASSINATURA'

# Tempo de expiração (em segundos)
expires_in_seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 30

# Payload do token
payload = {
    'service': 'service-a',
    'timestamp': datetime.utcnow().isoformat(),
    'purpose': 'inter-service-communication',
    'exp': datetime.utcnow() + timedelta(seconds=expires_in_seconds)
}

# Gerar token
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

print('\n🔑 JWT Token Gerado com Sucesso!\n')
print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
print('Token:')
print(token)
print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

print('📋 Informações:')
print(f'   Expira em: {expires_in_seconds} segundos')
print(f'   Algoritmo: HS256')
print(f'   Payload: {payload}')

print('\n💡 Como usar:\n')
print(f'   # Com curl:')
print(f'   curl -H "Authorization: Bearer {token}" http://localhost:8000/minha-rota\n')

print(f'   # Com PowerShell:')
print(f'   $headers = @{{ "Authorization" = "Bearer {token}" }}')
print(f'   Invoke-RestMethod -Uri "http://localhost:8000/minha-rota" -Headers $headers\n')

# Decodificar token para mostrar
decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
print('🔍 Token decodificado:')
print(f'   Payload: {decoded}')
print(f'   Expira em: {datetime.fromtimestamp(decoded["exp"]).isoformat()}')
