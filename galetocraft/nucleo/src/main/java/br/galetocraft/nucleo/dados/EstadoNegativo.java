package br.galetocraft.nucleo.dados;

/** Estados negativos persistentes (regra estados_negativos). Um por Galeto; suspensos na reserva. */
public enum EstadoNegativo {
	QUEIMADURA("Queimadura"), ENVENENAMENTO("Envenenamento"), AFOGAMENTO("Afogamento"), TONTO("Tonto"), PARALISIA("Paralisia");

	private final String nome;

	EstadoNegativo(String nome) {
		this.nome = nome;
	}

	public String nome() {
		return nome;
	}

	/** Aceita o nome oficial e o antigo ("Tontura" é alias técnico de Tonto). */
	public static EstadoNegativo deTexto(String texto) {
		String chave = Elemento.normalizar(texto);
		if (chave.equals("tontura"))
			return TONTO;
		for (EstadoNegativo e : values())
			if (Elemento.normalizar(e.nome).equals(chave))
				return e;
		throw new IllegalArgumentException("Estado desconhecido: " + texto);
	}
}
