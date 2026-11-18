# Galetocraft (mod Fabric + GeckoLib)

Cocorídeos para o Minecraft **1.21.11**. O mod traz 12 espécies do Galetário com modelos GeckoLib: #001 Pirococó, #003 Esporocó, #004 Cocórak, #005 Cocórion, #006 Cocórvolt, #007 Taturico, #008 Axococó, #009 Vagaló, #010 Morcegalo, #011 Espinhocó, #012 Salambrasa e #019 Renacocó.

Por enquanto as criaturas só aparecem por ovo gerador ou `/summon`. Cada uma é um Galeto individual, com nível, sexo e IVs. Já dá para capturar Galetos com a Pena de Captura e jogar Rinhas contra Galetos selvagens (veja abaixo). Os efeitos especiais dos golpes, as passivas, a XP dos Galetos e a reprodução ainda não estão implementados; as regras deles estão documentadas na base vigente (ver `../docs/CONHECIMENTO_GALETOCRAFT.md`).

Licença: todos os direitos reservados (ver `LICENSE`).

## Versões
| Item | Versão |
|---|---|
| Minecraft | 1.21.11 |
| Fabric Loader | 0.20.1 |
| Fabric API | 0.141.6+1.21.11 |
| GeckoLib (Fabric) | 5.4.5 |
| Java para rodar o Gradle | 25 (Eclipse Temurin), exigido pelo Loom 1.19 |
| Java do mod (alvo) | 21, o mesmo do Minecraft 1.21.11 |

## Compilar
No terminal, dentro desta pasta, com o Java 25 ativo:

```
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-25.0.5.8-hotspot
gradlew build
```

O arquivo do mod sai em `build/libs/galetocraft-0.1.0.jar`.

Para abrir o jogo de teste já com o mod: `gradlew runClient`.

## Jogar com o mod (instalação normal)
1. Instale o **Fabric Loader** para a 1.21.11 (https://fabricmc.net/use/installer/).
2. Coloque na pasta `mods` do Minecraft:
   - `galetocraft-0.1.0.jar` (deste projeto)
   - **Fabric API** para 1.21.11
   - **GeckoLib** (Fabric) 5.4.5 para 1.21.11
3. No jogo, os **ovos geradores** das 12 espécies ficam na aba de ovos geradores do modo criativo.

## Capturar e jogar Rinhas (versão de teste)
1. **Início da jornada:** ao entrar no mundo você recebe a Pena de Captura e escolhe um dos 6 iniciais pelos botões do chat (ou `/galetocraft inicial <1-6>`). Se a Pena se perder, ela volta ao entrar no mundo, renascer ou acordar (ou com `/galetocraft pena`).
2. **Captura no mundo:** com a Pena na mão, mire num Galeto a até 12 blocos e clique com o botão direito. Se falhar, ele resiste por 20 s (60 s se Lendário).
3. **Rinha:** chegue a até 10 blocos de um Galeto e use `/galetocraft desafiar`. Entram os 3 primeiros da sua equipe. Sem Galetos, entra a equipe de teste (`/galetocraft equipe teste cocorrego pirococo esporoco`).
4. Jogue clicando nos botões do chat: golpes (Combate), troca (Galetos), Mira, Guarda, Pena de Ritmo (depois de uma Concentração), Itens → Pena de Captura e Fugir.
5. Vencer uma Rinha dá XP aos seus Galetos que entraram em campo; eles sobem de nível pela curva oficial.
6. `/galetocraft equipe` mostra a equipe principal (até 5), as reservas, a XP de cada Galeto e a Pena, com botões para ver golpes, guardar, chamar e pôr em primeiro.
7. `/galetocraft golpes <n>` mostra os golpes equipados e aprendidos do Galeto e troca os slots livres fora da Rinha (a Concentração é fixa). Ao subir de nível, o Galeto aprende golpes novos, mas não os equipa sozinho.
8. Com mais de 3 Galetos, `/galetocraft desafiar` abre a **escalação**: escolha 3 e quem começa.
9. `/galetocraft companheiro <n>` chama um Galeto para seguir você; toque nele com a Pena (ou use `/galetocraft recolher`) para recolher. `/galetocraft libertar <n>` solta um Galeto para sempre, com confirmação dupla.
10. Os Galetos aparecem sozinhos no mundo, conforme bioma e horário, com nível de 1 a 70. Operadores podem usar `/galetocraft dar <espécie> [nível]`.

Outros comandos: `/galetocraft ficha <espécie>`, `/galetocraft base`, `/galetocraft rinha <a> <b> [nível]` (Rinha simulada) e `/galetocraft duelo <a> <b> [rinhas]` (operadores). Clicar num Galeto com a mão vazia mostra a ficha dele.

## Testes
- Regras (núcleo): `gradlew :nucleo:test`.
- Testes no cliente: `gradlew runClientGameTest`. A variável `GALETO_TESTES` escolhe quais rodam (`pirococo`, `galeria`, `rinha`, `captura`, `jornada`); sem ela, rodam todos. O `rinha` joga uma Rinha inteira pelos botões do chat; o `captura` captura no mundo com o botão direito e na Rinha pelo menu.
- Sem placa de vídeo (Linux): `GALETO_TESTES=rinha,captura LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a bash gradlew runClientGameTest`.

## Onde fica cada coisa
`<id>` é o nome técnico da espécie: `pirococo`, `esporoco`, `cocorak`, `cocorion`, `cocorvolt`, `taturico`, `axococo`, `vagalo`, `morcegalo`, `espinhoco`, `salambrasa` ou `renacoco`.

| O quê | Arquivo |
|---|---|
| Comportamento do Pirococó | `src/main/java/br/galetocraft/entidade/PirococoEntity.java` |
| Comportamento das demais espécies e dados do Galeto individual | `src/main/java/br/galetocraft/entidade/GaloEntity.java` |
| Comandos `/galetocraft` | `src/main/java/br/galetocraft/comando/ComandoGaletocraft.java` |
| Rinha jogável (sessões e menu do chat) | `src/main/java/br/galetocraft/rinha/` |
| Pena de Captura e captura | `src/main/java/br/galetocraft/captura/` |
| Equipe e reservas do treinador (salvas com o jogador) | `src/main/java/br/galetocraft/treinador/` e `registro/ModAnexos.java` |
| Regras do jogo (núcleo em Java puro) e dados da base | `nucleo/` |
| Registro das criaturas, da caixa de colisão, da vida, da velocidade e do dano | `src/main/java/br/galetocraft/registro/ModEntidades.java` |
| Registro dos ovos | `src/main/java/br/galetocraft/registro/` |
| Desenho, LOD e brilho | `src/client/java/br/galetocraft/client/` (`GaloRenderer`, `BrilhoParcialGeoLayer`) |
| Modelo 3D (formato GeckoLib/Bedrock) | `src/main/resources/assets/galetocraft/geckolib/models/entity/<id>.geo.json` |
| Animações (parado, andando) | `src/main/resources/assets/galetocraft/geckolib/animations/entity/<id>.animation.json` |
| Textura | `src/main/resources/assets/galetocraft/textures/entity/<id>.png` |
| Partes que brilham no escuro | `src/main/resources/assets/galetocraft/textures/entity/<id>_glowmask.png` |
| Nomes no jogo | `src/main/resources/assets/galetocraft/lang/pt_br.json` e `en_us.json` |

## Atualizar um modelo
Cada espécie tem um gerador em `../ferramentas/especies/<id>.py`. Na raiz do repositório, rode:

```
python ferramentas/especies/<id>.py
python ferramentas/exportar_especie.py <id>
```

1. O primeiro comando gera `modelos/<id>/<id>.bbmodel` e a máscara de brilho.
2. O segundo exporta o modelo, a animação e as texturas para o mod. Ele também otimiza o modelo e separa os ossos `_brilho` e `_lod`.
   - `--sem-otimizar` e `--sem-lod` desligam essas etapas.
   - `ferramentas/lod_auto.py <id>` recalcula `modelos/<id>/lods.json`.
3. Ovos e nomes de espécies novas são gerados por `ferramentas/registrar_especies.py`.

O fluxo antigo, com `pirococo6.py` e `exportar_geckolib.py`, está obsoleto. Esses scripts ficam só como histórico.
