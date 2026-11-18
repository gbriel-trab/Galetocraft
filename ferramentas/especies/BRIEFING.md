# Briefing: modelar uma criatura do Galetocraft (mesmo procedimento do Pirococó)

> **Desde 18/11/2026, o padrão visual é `modelos/GUIA_ESTILO.md` (estilo Cobblemon).** Leia o guia antes deste
> briefing. Onde as regras técnicas daqui conflitam com ele, vale o guia: orçamento, tamanho da textura, UV de
> caixa, planos, luz pintada e volumes arredondados (seção 9 do guia). O resto continua valendo: procedimento,
> fidelidade à ficha, nomes de ossos e critérios do revisor.

## Objetivo
Escrever `ferramentas/especies/<id>.py`, um gerador em Python que constrói a criatura da ficha como modelo
Minecraft Java (cubos do Blockbench, formato Bedrock, para o GeckoLib) com textura pintada em 3D. O alvo é ficar
o mais fiel possível à ficha, com o acabamento do Pirococó (que o dono já aprovou).

## Onde está cada coisa
- **Ficha da sua criatura** (o alvo) em `modelos/referencias/`:
  - `<NNN_id>_ficha.png` (ficha inteira);
  - `_arte.png` (arte principal);
  - `_vistas.png` (frente, lateral direita, traseira, lateral esquerda);
  - `_detalhes.png` e `_expressoes.png` (o Cocórak não tem esses dois, só a arte e as vistas).
- **Nível de qualidade esperado** (o Pirococó aprovado):
  - imagens: `modelos/pirococo/pirococo_melhor_vistas.png`, `pirococo_melhor_3-4.png` e `pirococo_rosto.png`;
  - código: `ferramentas/pirococo7.py`. Leia-o para ver as técnicas na prática: rosto facetado com o olho numa
    face plana, bico em cunha com gancho, penas recortadas em leque, chamas em X, armadura facetada e correntes.
- **Biblioteca comum**: `ferramentas/galo_base.py`. Leia o docstring e as funções. Ela tem Peca/peca/osso,
  materiais pintados em 3D, formas prontas, `pintar_olho`, `gerar()`, `revisao()` e `rodar()`.

## Regras
- Escreva SÓ no seu arquivo `ferramentas/especies/<id>.py` e em `modelos/<id>/`. Arquivos temporários vão para
  `modelos/<id>/revisao/`.
- NÃO altere `galo_base.py`, `previa*.py`, `pirococo7.py`, as outras espécies nem nada em `galetocraft/`. Se
  precisar de uma função nova, ponha-a no seu arquivo.
- Não rode Gradle nem Minecraft, não instale nada, não baixe nada.
- Identificadores e comentários em português, no estilo de `pirococo7.py`.

## Esqueleto do arquivo
```python
"""<Nome> (#NNN, tipo): uma linha sobre a criatura."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp   # etc.

ID = "<id>"; NOME = "<Nome com acento>"; NUMERO = NNN
ALTURA = 2.45            # altura visível no jogo, em blocos (o exportador escala para isso)
QUADRUPEDE = False       # True só para quem anda em 4 patas
ROSTO = ((0, 25, -2), 6) # centro (x, y, z) e raio do close do rosto em revisao/atual_rosto.png
ONDAS = []               # cadeias que ondulam sozinhas: [(prefixo_dos_ossos, n_segmentos, (amp_rx, amp_ry, amp_rz))]
ANIM_PARADO = {}         # extras: {"nome_do_osso": [(rx, ry, rz), ...]} (graus como no Blockbench,
ANIM_ANDANDO = {}        #  keyframes igualmente espaçados, o último igual ao primeiro)

def montar():
    ...
    return [corpo, perna_d, perna_e]   # lista de ossos raiz

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
```

Para rodar, use `python ferramentas/especies/<id>.py`. Ele grava `modelos/<id>/<id>.bbmodel`, a textura e o
`_glowmask`, e as imagens `modelos/<id>/revisao/atual_vistas.png`, `atual_3-4.png` e `atual_rosto.png`.
Para guardar uma rodada, passe pasta e prefixo: `python ferramentas/especies/<id>.py modelos/<id>/revisao r3`.

## Nomes de ossos que o jogo anima (use exatamente estes)
O exportador já anima estes nomes sozinho: respiração e olhar quando parado, passo quando anda.
- `corpo`: osso raiz do tronco, com o pivô no quadril.
- `pescoco`: filho de `corpo`.
- `cabeca`: filho de `pescoco`.
- `crista`: opcional, filho de `cabeca`.
- Pernas, ossos raiz:
  - bípede: `perna_d` e `perna_e`;
  - quadrúpede: `perna_fd`, `perna_fe`, `perna_td`, `perna_te` (f = frente, t = trás, d = direita, e = esquerda).
- `asa_d` e `asa_e`: filhos de `corpo`.
- `cauda`: filho de `corpo`.

Cauda comprida, cipó, tentáculo e outras cadeias feitas com `g.pena_curva(nome, ...)` viram ossos `nome_0`,
`nome_1` e assim por diante. Para que ondulem, declare-as em `ONDAS`.

Outras partes que devem mexer sozinhas (orelhas, guelras, talismãs pendurados, chapéu) precisam de um osso com nome
próprio. Coloque a animação delas em `ANIM_PARADO` e `ANIM_ANDANDO`. Todo o resto pode ficar em ossos estáticos com
qualquer nome: o otimizador achata esses ossos na exportação.

## Tamanho e orçamento
- Modele no tamanho final: cerca de 39 unidades de altura para 2,45 blocos, como o Pirococó.
- Mantenha o modelo abaixo de ~350 peças e a textura até 512x1024.
- Peças miúdas e repetidas custam desempenho; prefira poucas peças bem desenhadas na textura.

## Como trabalhar
1. Leia a ficha inteira e anote proporções:
   - altura da cabeça em relação ao corpo;
   - comprimento das pernas;
   - tamanho da cauda;
   - silhueta de frente e de lado.
2. Monte primeiro a SILHUETA (volumes grandes) e compare as vistas com `_vistas.png` da ficha.
3. Depois faça a CABEÇA e o ROSTO: olho, bico, crista, barbela. É onde o dono mais repara.
   - O rosto não pode parecer "disforme". Ponha o olho inteiro numa face plana: um decalque dividido entre duas
     faces em degrau fica deformado. Use `pintar_olho` e veja como o Pirococó faz.
   - O bico não deve ser uma caixa pura: use base, meio e gancho em cunha, com degradê.
4. Por fim, os detalhes da ficha (padrões, emblemas, adereços) e a paleta (`Paleta de Cores` na ficha).
5. Itere muitas vezes, rodando e OLHANDO as imagens de revisão ao lado da ficha a cada rodada. Faça pelo menos
   8 rodadas. Corrija primeiro o que mais muda a semelhança.

## Lições do Pirococó
- Placas finas vistas de perfil viram um "toco". Para penas, chamas e folhas que aparecem de vários ângulos,
  use placas em X a 45° (`pena_cruzada` e `chama_cruzada`).
- Duas faces no mesmo plano piscam (z-fighting). Afaste uma da outra 0,02 a 0,05.
- Nada de pilhas de blocos empilhados: o modelo não pode parecer entulhado.
- Volumes orgânicos (tronco, cabeça, coxa) ficam melhores com `arredondado` e `arredondado2` do que como
  caixas puras.
- Pinte a luz em 3D (`mat_cor` já faz isso): claro em cima, sombra embaixo e fio escuro nas bordas. É o que dá
  o acabamento "Cobblemon".
- Partes que brilham no escuro usam `brilho=True` (ou uma função) e vão para a `_glowmask`. Exemplos: brasas,
  raios, olhos eletrificados, miolo de flor, vaga-lume.
- Cuidado com o sentido: a frente é -z e o lado direito da criatura é -x. Confira nas vistas com legenda.

## Critérios do revisor
Um diretor de arte independente vai comparar suas imagens com a ficha. Ele dá nota de 0 a 10 em:
1. silhueta, proporções e presença;
2. cabeça e rosto;
3. olhos e expressão;
4. bico, crista e barbela;
5. corpo e plumagem;
6. asas;
7. cauda;
8. pernas e pés;
9. elementos característicos da espécie (padrões, adereços, emblema);
10. cores, acabamento e limpeza.

Aprovado = todas as notas ≥ 7 e média ≥ 8. "Expressões" da ficha: modele só a NEUTRA. Atributos, golpes e
habilidades da ficha não fazem parte do modelo.

## Relatório final
Responda em até ~20 linhas:
- o que foi modelado e como cada elemento da ficha foi resolvido;
- número de peças e tamanho da textura;
- os ossos animáveis que você criou;
- o que ainda difere da ficha e por quê.
