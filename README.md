# Galetocraft

Projeto Galetocraft: código, modelos, ferramentas e acervo documental.

## Dados e documentos

O acervo documental de 17/11/2026 está na seção [Releases](/gbriel-trab/Galetocraft/releases/tag/acervo-documental-2026-11-17), com 1.636 arquivos identificados do projeto, inventário e somas SHA-256. Os pacotes são arquivos ZIP independentes: extraia todos na mesma pasta para reconstruir a organização original. Os arquivos relacionados que estavam fora da pasta Galetocraft são preservados na raiz da extração.

- **Galetocraft_00_Base_Vigente.zip**: banco vigente, manual, atualizador, verificação e índices.
- **Galetocraft_NN_Acervo.zip**: demais documentos, artes, scripts, propostas, estudos e históricos.
- **INVENTARIO_GALETOCRAFT.json**: caminho, tamanho, SHA-256 e pacote de cada arquivo.
- **SHA256SUMS.txt**: verificação dos pacotes ZIP.
- **DADOS_VIGENTES_CONSULTA.json**: exportação legível da camada atual; arquivo derivado, não uma base concorrente.

## Fonte de verdade

A única base documental vigente é `Galetocraft/Base_Atual/Galetocraft.sqlite`. Consulte `current_*` e `v_current_*`; a tabela `species` é legada. Betas, ramos R, propostas e ensaios são evidências históricas, mesmo quando o nome original contém 'oficial'. Em conflitos, prevalecem a camada vigente e as decisões posteriores comprovadas.

O banco exportado passou em `PRAGMA integrity_check` e contém 23 espécies, 690 vínculos de golpes e 21 artes. SHA-256: `9dd2253deabb2732cb8815a6cb7a50944bca29a57cb0bf421cf1d48e89e5aa3c`.

## Implementação e atualização

As pastas `galetocraft`, `modelos`, `ferramentas` e `benchmark` existentes no repositório foram preservadas. A publicação documental não comprova que todas as regras já estejam implementadas ou testadas no Minecraft.

Este envio é uma fotografia dos arquivos identificados e acessíveis em 17/11/2026. Não configura sincronização automática. Não inclui conversas não exportadas nem anexos cuja relação com o projeto não pôde ser identificada. Para atualizar dados, siga `LEIA_ME_Base_Unica.md`, preserve a identidade da base e registre fonte, revisão e validações.

