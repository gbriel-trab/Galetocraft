# Modelo do prompt de correção

Este é o esqueleto que eu (o chat de planejamento) preencho a cada rodada, a partir da imagem do resultado que o
dono traz. A versão preenchida vai para `prompts/correcoes/<id>_cNN.md` e é colada **na mesma conversa** em que o
modelo foi feito, porque o outro chat já tem o script gerador.

## Como eu diagnostico antes de escrever

1. **Silhueta contra a ficha e o plano de proporções.** Confiro a altura dos marcos, as larguras, o perfil em S, a
   capa, a cauda e as pernas. Se vierem os arquivos, renderizo com `ferramentas/render_geo.py` e meço. Se vier só
   imagem, comparo na mesma escala.
2. **DNA Cobblemon** (seção B do prompt mestre):
   - 1 px por unidade e mixels;
   - entulho;
   - curva falsa;
   - contorno preto ou degradê liso;
   - planos que piscam ou somem;
   - rosto.
3. **Elementos característicos da criatura:** as contagens e a ordem das camadas.
4. **Cor e acabamento.**
5. **Animação**, se o dono mandar vídeo ou mais de um quadro.
6. **Prioridade:** escolho os **5 a 8 problemas que mais mudam a semelhança**. Correções demais de uma vez geram
   regressões. O resto fica para a rodada seguinte.
7. **Formato de cada item:** digo como está, como deve ficar (com número: u, px, graus, cor em hex), como fazer e
   como conferir.

---

## Esqueleto (o que vai para o outro chat)

```markdown
# Correção {{N}} — {{NOME}} ({{ID}})

Continue o MESMO modelo desta conversa, a partir do seu `gerar_{{ID}}.py`. Não recomece do zero: mude só o que
está listado abaixo e preserve todo o resto. As regras do pedido original continuam valendo (1 px por unidade,
cubos de tamanho inteiro, planos com uma face só, paleta, nomes de ossos e de animações).

Anexo: a imagem de como o modelo ficou. Use-a para localizar cada problema.

## O que está bom (NÃO mexer)
- ...

## Problemas, do mais grave para o menos grave

### 1. <área>
- **Como está:** <descrição objetiva, com medida quando der>
- **Como deve ficar:** <alvo com números>
- **Como fazer:** <técnica>
- **Aceite:** <o que precisa aparecer no render>

### 2. ...

## Ordem de trabalho
1. Corrija os itens na ordem, renderizando e OLHANDO depois de cada um.
2. Não piore o que está na lista "NÃO mexer". Confira lado a lado com a versão anterior.
3. Rode de novo todas as validações do script.

## Entregue
- os mesmos arquivos atualizados (`.geo.json`, `.png`, `_glowmask.png`, `.animation.json`, `gerar_{{ID}}.py`);
- `{{ID}}_vistas.png`, `{{ID}}_rosto.png` e `{{ID}}_antes_depois.png` (vistas antigas em cima, novas embaixo);
- uma lista curta: item → o que mudou (com números) → resolvido ou parcial (e por quê).
```
