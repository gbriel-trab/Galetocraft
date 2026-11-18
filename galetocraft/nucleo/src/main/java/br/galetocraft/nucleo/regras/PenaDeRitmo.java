package br.galetocraft.nucleo.regras;

/**
 * Pena de Ritmo da Concentração V2.3 (regra concentracao, itens 3 a 8).
 * <ul>
 * <li>Uma Pena por equipe, criada ao fim de uma Concentração válida quando a equipe não tem nenhuma.</li>
 * <li>Não pode ser usada na mesma ação em que foi criada.</li>
 * <li>Vale nas duas próximas oportunidades próprias da equipe e expira depois delas.</li>
 * <li>Concentração repetida não cria outra Pena nem renova a validade.</li>
 * <li>Continua se o Galeto que a criou sair ou for derrotado, enquanto a equipe estiver apta.</li>
 * </ul>
 */
public final class PenaDeRitmo {
	public static final int VALIDADE = 2;

	public enum Canto {
		/** +12% de dano no 1º acerto direto válido e +6 de Pressão. */
		OFENSIVO,
		/** +15 de Energia se a Guarda localizada estiver correta e houver dano ao HP. */
		GUARDA,
		/** −20% no primeiro acerto ofensivo direto sofrido pelo Galeto que entrou. */
		REVEZAMENTO,
		/** −15 no custo de um Suporte que não seja Concentração. */
		SUPORTE
	}

	private boolean ativa;
	private boolean recemCriada;
	private int oportunidadesRestantes;

	public boolean ativa() {
		return ativa;
	}

	/** Chamado ao fim de uma Concentração válida. Devolve {@code true} se criou a Pena. */
	public boolean aoConcentrar() {
		if (ativa)
			return false;
		ativa = true;
		recemCriada = true;
		oportunidadesRestantes = VALIDADE;
		return true;
	}

	/** Pode ser declarada nesta ação? (não na ação em que foi criada) */
	public boolean disponivel() {
		return ativa && !recemCriada;
	}

	/** Consome a Pena (o momento do consumo depende do Canto, ver a ata). */
	public void consumir() {
		if (!disponivel())
			throw new IllegalStateException("Pena de Ritmo indisponível");
		ativa = false;
	}

	/** Fim de uma oportunidade própria da equipe. */
	public void fimDaOportunidade() {
		if (!ativa)
			return;
		if (recemCriada) {
			recemCriada = false;
			return;
		}
		if (--oportunidadesRestantes <= 0)
			ativa = false;
	}

	/** Fim da Rinha ou equipe sem Galetos aptos. */
	public void encerrar() {
		ativa = false;
	}
}
