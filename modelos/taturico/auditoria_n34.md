# Auditoria de detalhes: Taturico (007_taturico), rodada n34

## TOP 10 PROBLEMAS

1. **Padrão e paleta da carapaça (corpo, asas e topo do elmo; todas as vistas)**
   - **Modelo:** textura "camuflada", com manchas aleatórias e muitos pixels marrom quase preto (#301000 a #401010). Os tons claros são um tan acinzentado e oliva (#907040, #b08050). Não dá para ver bandas.
   - **Ficha:** cada placa é uma faixa limpa de duas cores. Metade marrom-malva (#5a2f29 a #8f4f3f) e metade laranja-tan saturado (#ed9f5e / #cd743e). Ao longo da faixa há um xadrez regular de blocos grandes. Na traseira são arcos horizontais empilhados: marrom em cima, laranja embaixo.
   - **Correção:**
     - Retexturizar todas as placas com bandas: ~50% marrom #8f4f3f/#5a2f29 e ~50% laranja #ed9f5e/#cd743e, com xadrez de blocos de 2x2 px.
     - Eliminar todo pixel mais escuro que #572d27.
     - Trocar os tans oliva pelos laranjas da paleta.
     - O topo do elmo segue a mesma regra.

2. **Forma da carapaça (lateral e traseira)**
   - **Modelo, de lado:** perfil em "escada" de degraus retos. A borda inferior é plana e baixa.
   - **Modelo, de trás:** caixa retangular com as asas como painéis chatos abertos em trapézio. Sobra muito nos ombros, o azul do comp.
   - **Ficha, de lado:** arco contínuo de 5 ou 6 placas curvas sobrepostas, como as cintas de um tatu. Vai da nuca até a ponta da cauda, e cada placa se sobrepõe à seguinte.
   - **Ficha, de trás:** corpo em forma de ovo ou pinha, mais estreito no topo, mais largo no meio e afunilando até a cauda.
   - **Correção:**
     - Arredondar o dorso com placas inclinadas em leque, cada uma 1 a 2 px mais baixa e recuada que a anterior, no lugar dos degraus.
     - De trás, recolher os painéis das asas ~2 px para dentro em cima e fechar a base, para formar o ovo.

3. **Cauda blindada (lateral e traseira)**
   - **Modelo:** toco rombudo e baixo, que termina reto na altura da barriga. De trás, não aparece como cone.
   - **Ficha:** cone longo de 4 ou 5 anéis decrescentes, cada anel com banda marrom e laranja. Termina em ponta laranja afiada, apontada para trás e para baixo, na altura do meio da perna. De trás, o cone desce no centro entre as pernas até quase o chão.
   - **Correção:**
     - Fazer 4 ou 5 anéis encaixados, cada um ~2 px menor de seção que o anterior.
     - Inclinar ~25° para baixo e terminar em uma ponta de 1x1 a 2x2 px.
     - Alongar ~30% para trás. É onde o comp mostra o vermelho, que indica a parte que falta.

4. **Rosto: área em volta dos olhos (frente e lado)**
   - **Modelo:** mancha marrom-escura (~#4a2a1a) em volta de cada olho, como uma máscara ou olheira.
   - **Ficha (neutra):** o rosto em volta do olho é creme e bege claro (#fcdfbe com sombra bege-acinzentada). Só há uma linha fina marrom sob o olho, a pálpebra inferior. O escuro acima do olho vem apenas da aba do elmo.
   - **Correção:**
     - Pintar todo o entorno do olho de creme #fcdfbe.
     - Deixar só 1 px marrom #8f4f3f na pálpebra inferior.

5. **Bico (frente e lado)**
   - **Modelo, de frente:** pequeno e estreito, uma tira amarela de ~1/6 da largura do rosto.
   - **Modelo, de lado:** curto, dois blocos com um torto, sem narina.
   - **Ficha, de frente:** bico grande em trapézio. A largura no topo é ~1/3 do rosto e afina para baixo. Começa logo abaixo da aba do elmo e a ponta encosta no topo das barbelas.
   - **Ficha, de lado:** cunha longa, comprimento ~2x o diâmetro do olho. A mandíbula superior é curvada para baixo na ponta. O topo é amarelo vivo #fca702 / #f7bc0a, a parte de baixo é laranja, e há uma narina preta quadrada (1 px) no topo, perto da base.
   - **Correção:**
     - Aumentar o bico ~1,5x em largura e ~1,6x em comprimento.
     - Ponta com gancho de 1 px para baixo.
     - Adicionar a narina preta.
     - Amarelo mais vivo, sem o tom mostarda #b0a010.

6. **Olho (forma e cor; frente e lado)**
   - **Modelo:** olho amendoado e "zangado", com a íris âmbar-laranja escura (#c07000).
   - **Ficha (neutra):** olho redondo com íris amarelo-dourado #f7bc0a que ocupa a maior parte do olho. A pupila preta é grande, centrada para a frente, com brilho branco de 1 px. A esclera creme/branca aparece no lado de trás. A aba do elmo cobre o topo do olho; o olho em si não é inclinado.
   - **Correção:**
     - Desenhar o olho redondo, com a íris #f7bc0a.
     - Pupila preta de ~40% do olho, com brilho branco.
     - Esclera clara atrás.
     - O ar severo deve vir só da aba sobre o olho.

7. **Pernas e pés (todas as vistas)**
   - **Modelo:**
     - As pernas são âmbar/laranja escuro (#c57a0b).
     - Os dedos são cubos cinza colados direto sob a perna, sem parte amarela.
   - **Ficha (Patas Fortes):**
     - Pernas grossas amarelo vivo #fca702.
     - Pé amarelo com 3 dedos amarelos para a frente, cada um com uma garra cinza-malva (#7f5e67) grande na ponta, de ~metade do comprimento do dedo.
     - Há também uma garra cinza traseira.
   - **Correção:**
     - Pintar pernas e pés de #fca702.
     - Fazer cada dedo com a base amarela de ~2 px e a garra cinza #7f5e67 na ponta.
     - Manter a garra traseira.

8. **Emblema da carapaça (placa da asa; lateral)**
   - **Modelo:** linhas finas de cantos arredondados que formam um "arco/cogumelo" mole, em tan apagado.
   - **Ficha:**
     - Moldura quadrada grossa laranja-tan (#ed9f5e), com ~1/8 da largura da placa, sobre o fundo marrom-malva.
     - Dentro, um meandro de cantos retos, em forma de "Ǝ/ш": barra inferior e laterais laranja, com um dente escuro central descendo do topo.
     - Linhas tão grossas quanto a moldura.
   - **Correção:**
     - Redesenhar em grade, só com ângulos retos e traço de 2 px na textura.
     - Usar laranja #ed9f5e sobre #8f4f3f e eliminar todo canto arredondado.

9. **Barbelas (frente e lado)**
   - **Modelo:** duas tiras vermelhas finas, bem abertas em "V".
   - **Ficha:**
     - Duas placas vermelhas largas, cada uma com ~a largura do bico. Pendem quase verticais, divergindo pouco, e descem até o meio do peito.
     - Cor #cf2523.
     - De lado, formam um bloco vermelho robusto sob o bico.
   - **Correção:**
     - Dobrar a largura de cada barbela.
     - Reduzir a abertura para ~10° da vertical.
     - Alongar até o meio do peito.

10. **Placas laterais do elmo, as "bochechas" (frente e lado)**
    - **Modelo, de frente:** placas nos cantos superiores da cabeça, na altura da testa/aba.
    - **Modelo, de lado:** placa quadrada com espiral.
    - **Ficha, de frente:** as placas ficam mais baixas, da altura do olho até a base do bico. Ladeiam o rosto e se projetam para a frente.
    - **Ficha, de lado:** a face lateral é um retângulo horizontal com moldura laranja e uma fenda escura central. A espiral angular só aparece na face frontal.
    - **Correção:**
      - Descer as placas ~metade da própria altura.
      - Na face lateral, usar o desenho de moldura com fenda retangular.
      - Manter o meandro quadrado na face frontal.

## OUTROS PROBLEMAS MENORES
- Há linhas finas claras horizontais (z-fighting ou lascas de cubo) espalhadas pela carapaça nas vistas lateral e traseira.
- Na vista isolada da cabeça (`_rosto`, de lado), placas finas soltas se projetam horizontalmente para trás da nuca.
- Os painéis das asas na frente abrem em trapézio para fora embaixo. Na ficha, a asa desce reta, quase colada ao peito.
- No elmo, a aba em "V" frontal está clara demais (tan); na ficha ela é predominantemente marrom-malva, com blocos laranja.
- O peito/babador está em tom bege-acinzentado (#c0a080). Na ficha é creme mais quente (#fcdfbe), com sombra suave.
- A garra cinza do modelo está um pouco escura e roxa. A da ficha é cinza-malva #7f5e67, mais clara.
- A crista de lado está ligeiramente baixa e curta. Na ficha, ela se inclina para trás em 3 degraus mais altos.

## O QUE JÁ ESTÁ FIEL
- A crista de frente e de trás tem a cruz de 5 blocos vermelhos, correta.
- A aba do elmo em "V" sobre os olhos dá a expressão severa da ficha.
- O peito creme em camadas termina em uma franja de penas verticais, como na ficha.
- A placa grande da asa está no tamanho e na posição corretos, no meio do corpo.
- A proporção geral (cabeça embutida no corpo, pernas curtas e grossas) e o IoU de silhueta de ~88% estão bons.

## NOTA DE FIDELIDADE AOS DETALHES
**5/10.** Dos 10 problemas principais, 5 são de rosto (4, 5, 6, 9 e 10).
