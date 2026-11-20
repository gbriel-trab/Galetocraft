# Galetocraft (mod Fabric + GeckoLib)

Galos lendários para o Minecraft **1.21.11**.

**Estado em 20/11/2026:** o mod não tem nenhuma criatura registrada. Os 12 modelos antigos (Pirococó, Esporocó,
Cocórak, Cocórion, Cocórvolt, Taturico, Axococó, Vagaló, Morcegalo, Espinhocó, Salambrasa e Renacocó) saíram do
jogo a pedido do dono, para dar lugar aos modelos novos. Os arquivos-fonte deles continuam em `../modelos/` e
`../ferramentas/especies/`.

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
3. No jogo, o ovo gerador de cada criatura fica na aba de ovos geradores do modo criativo.

## Onde fica cada coisa
| O quê | Arquivo |
|---|---|
| Comportamento (vida, ataque, IA, sons) | `src/main/java/br/galetocraft/entidade/GaloEntity.java` |
| Registro das criaturas e dos ovos | `src/main/java/br/galetocraft/registro/` |
| Desenho, brilho e LOD | `src/client/java/br/galetocraft/client/GaloRenderer.java` e `BrilhoParcialGeoLayer.java` |
| Modelo 3D (formato GeckoLib/Bedrock) | `src/main/resources/assets/galetocraft/geckolib/models/entity/<id>.geo.json` |
| Animações (parado, andando) | `src/main/resources/assets/galetocraft/geckolib/animations/entity/<id>.animation.json` |
| Textura | `src/main/resources/assets/galetocraft/textures/entity/<id>.png` |
| Partes que brilham no escuro | `src/main/resources/assets/galetocraft/textures/entity/<id>_glowmask.png` |
| Ovo gerador | `items/<id>_spawn_egg.json`, `models/item/<id>_spawn_egg.json` e `textures/item/<id>_spawn_egg.png` |
| Nome no jogo | `src/main/resources/assets/galetocraft/lang/pt_br.json` e `en_us.json` |

## Colocar uma criatura no jogo
1. Ponha o modelo, as animações (`animation.<id>.idle` e `animation.<id>.walk`), a textura e a `_glowmask` nos caminhos
   da tabela acima.
2. Registre a espécie com uma linha `galo("<id>", ...)` em `ModEntidades.java`. O ovo gerador e o desenho são
   registrados sozinhos a partir dessa lista.
3. Crie o ovo gerador e os nomes (`entity.galetocraft.<id>` e `item.galetocraft.<id>_spawn_egg`).
   `../ferramentas/registrar_especies.py` faz isso para as espécies da lista dele.
